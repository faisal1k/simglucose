import math
import random
from ..base import SimulationEngineBase
from ..models import BasalProfile, PatientProfile, SimulationConfig, SimulationResult


class SimplifiedEngine(SimulationEngineBase):
    model_version = "simplified-v1"

    def run(self, patient: PatientProfile, config: SimulationConfig, seed: int | None = None) -> SimulationResult:
        if seed is not None:
            random.seed(seed)

        basal = BasalProfile(units_per_hour=patient.basal_rate_u_per_hr)
        dt = config.time_step_min
        points: list[dict] = []

        glucose = config.starting_glucose_mgdl
        active_carbs = [(m.time_min, m.carbs_g) for m in config.meals]
        active_bolus = [(b.time_min, b.units) for b in config.boluses]
        in_hypo = False
        in_hyper = False
        hypo_events = 0
        hyper_events = 0

        for t in range(0, config.duration_min + dt, dt):
            meal_carbs_now = sum(carbs for tm, carbs in active_carbs if tm == t)
            bolus_now = sum(units for tm, units in active_bolus if tm == t)
            basal_units = basal.units_per_hour * (dt / 60)

            carbs_on_board = self._carbs_on_board(active_carbs, t, patient.carb_absorption_duration_min)
            insulin_on_board = self._insulin_on_board(active_bolus, t, patient.insulin_action_duration_min)

            carb_glucose_rise = self._carb_effect(active_carbs, t, patient, dt)
            insulin_glucose_drop = self._insulin_effect(active_bolus, t, patient, dt, basal_units)
            baseline_pull = ((patient.baseline_glucose_mgdl - glucose) * patient.glucose_effectiveness * (dt / 60))
            noise = random.gauss(0, patient.variability_noise_std + config.disturbance_std)

            glucose = max(35.0, min(500.0, glucose + carb_glucose_rise - insulin_glucose_drop + baseline_pull + noise))

            if glucose < 70 and not in_hypo:
                hypo_events += 1
                in_hypo = True
            elif glucose >= 75:
                in_hypo = False
            if glucose > 180 and not in_hyper:
                hyper_events += 1
                in_hyper = True
            elif glucose <= 170:
                in_hyper = False

            points.append({
                "t_min": t,
                "glucose_mgdl": round(glucose, 2),
                "insulin_on_board_u": round(insulin_on_board, 2),
                "carbs_on_board_g": round(carbs_on_board, 2),
                "basal_units_delivered": round(basal_units, 3),
                "bolus_units_delivered": round(bolus_now, 3),
                "meal_carbs_ingested": round(meal_carbs_now, 2),
            })
        return SimulationResult(points=points, summary=self._summary(points, hypo_events, hyper_events), model_version=self.model_version)

    def _carb_effect(self, meals, t, p, dt):
        total = 0.0
        for mt, carbs in meals:
            elapsed = t - mt
            if elapsed < 0 or elapsed > p.carb_absorption_duration_min:
                continue
            x = elapsed / p.carb_absorption_duration_min
            absorption = math.exp(-((x - 0.45) ** 2) / 0.08)
            glucose_per_gram = p.insulin_sensitivity_factor / p.carb_ratio
            total += carbs * glucose_per_gram * absorption * (dt / p.carb_absorption_duration_min)
        return total

    def _insulin_effect(self, boluses, t, p, dt, basal_units):
        total = 0.0
        for bt, units in boluses:
            elapsed = t - bt
            if elapsed < 0 or elapsed > p.insulin_action_duration_min:
                continue
            x = elapsed / p.insulin_action_duration_min
            action = math.exp(-((x - 0.5) ** 2) / 0.05)
            total += units * p.insulin_sensitivity_factor * action * (dt / p.insulin_action_duration_min)
        return total + basal_units * p.insulin_sensitivity_factor * 0.2

    def _carbs_on_board(self, meals, t, absorption_min):
        return sum(carbs * (1 - ((t - mt) / absorption_min)) for mt, carbs in meals if 0 <= (t - mt) < absorption_min)

    def _insulin_on_board(self, boluses, t, action_min):
        return sum(units * (1 - ((t - bt) / action_min)) for bt, units in boluses if 0 <= (t - bt) < action_min)

    def _summary(self, points, hypo_events, hyper_events):
        vals = [p["glucose_mgdl"] for p in points]
        in_range = [v for v in vals if 70 <= v <= 180]
        return {
            "average_glucose": round(sum(vals) / len(vals), 2),
            "peak_glucose": round(max(vals), 2),
            "minimum_glucose": round(min(vals), 2),
            "time_in_range_percent": round((len(in_range) / len(vals)) * 100, 2),
            "hypo_events": hypo_events,
            "hyper_events": hyper_events,
        }
