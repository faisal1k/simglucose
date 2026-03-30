import math
import random
from .models import BasalProfile, MealEvent, PatientProfile, SimulationConfig, SimulationResult


class SimulationEngine:
    """Simplified glucose-insulin simulator with upgrade-friendly structure."""

    model_version = "simplified-v1"

    def run(self, patient: PatientProfile, config: SimulationConfig, seed: int | None = None) -> SimulationResult:
        if seed is not None:
            random.seed(seed)

        basal = BasalProfile(units_per_hour=patient.basal_rate_u_per_hr)
        dt = config.time_step_min
        points: list[dict] = []

        glucose = config.starting_glucose_mgdl
        active_carbs: list[tuple[int, float]] = [(m.time_min, m.carbs_g) for m in config.meals]
        active_bolus: list[tuple[int, float]] = [(b.time_min, b.units) for b in config.boluses]

        in_hypo = False
        in_hyper = False
        hypo_events = 0
        hyper_events = 0

        for t in range(0, config.duration_min + dt, dt):
            meal_carbs_now = sum(carbs for tm, carbs in active_carbs if tm == t)
            bolus_now = sum(units for tm, units in active_bolus if tm == t)

            correction_units = 0.0
            if config.correction_threshold_mgdl and glucose > config.correction_threshold_mgdl:
                correction_units = max(0.0, (glucose - config.target_glucose_mgdl) / patient.insulin_sensitivity_factor)
                correction_units *= 0.15

            basal_units = basal.units_per_hour * (dt / 60)

            carbs_on_board = self._carbs_on_board(active_carbs, t, patient.carb_absorption_duration_min)
            insulin_on_board = self._insulin_on_board(active_bolus, t, patient.insulin_action_duration_min)

            carb_glucose_rise = self._carb_glucose_effect(active_carbs, t, patient, dt)
            insulin_glucose_drop = self._insulin_glucose_effect(
                active_bolus, t, patient, dt, basal_units + correction_units
            )

            baseline_pull = (
                (patient.baseline_glucose_mgdl - glucose)
                * patient.glucose_effectiveness
                * (dt / 60)
            )

            exercise_boost = self._exercise_modifier(config, t)
            insulin_glucose_drop *= exercise_boost * patient.activity_sensitivity_modifier

            noise = random.gauss(0, patient.variability_noise_std + config.disturbance_std)

            glucose += carb_glucose_rise - insulin_glucose_drop + baseline_pull + noise
            glucose = max(35.0, min(500.0, glucose))

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

            points.append(
                {
                    "t_min": t,
                    "glucose_mgdl": round(glucose, 2),
                    "insulin_on_board_u": round(insulin_on_board, 2),
                    "carbs_on_board_g": round(carbs_on_board, 2),
                    "basal_units_delivered": round(basal_units, 3),
                    "bolus_units_delivered": round(bolus_now + correction_units, 3),
                    "meal_carbs_ingested": round(meal_carbs_now, 2),
                }
            )

        summary = self._summarize(points, hypo_events, hyper_events)
        return SimulationResult(points=points, summary=summary, model_version=self.model_version)

    def _carb_glucose_effect(
        self,
        meals: list[tuple[int, float]],
        t: int,
        patient: PatientProfile,
        dt: int,
    ) -> float:
        total = 0.0
        for meal_t, carbs in meals:
            elapsed = t - meal_t
            if elapsed < 0 or elapsed > patient.carb_absorption_duration_min:
                continue
            x = elapsed / patient.carb_absorption_duration_min
            absorption = math.exp(-((x - 0.45) ** 2) / 0.08)
            glucose_per_gram = patient.insulin_sensitivity_factor / patient.carb_ratio
            total += carbs * glucose_per_gram * absorption * (dt / patient.carb_absorption_duration_min)
        return total

    def _insulin_glucose_effect(
        self,
        boluses: list[tuple[int, float]],
        t: int,
        patient: PatientProfile,
        dt: int,
        basal_plus_correction_units: float,
    ) -> float:
        total = 0.0
        for bolus_t, units in boluses:
            elapsed = t - bolus_t
            if elapsed < 0 or elapsed > patient.insulin_action_duration_min:
                continue
            x = elapsed / patient.insulin_action_duration_min
            action = math.exp(-((x - 0.5) ** 2) / 0.05)
            total += units * patient.insulin_sensitivity_factor * action * (dt / patient.insulin_action_duration_min)

        total += basal_plus_correction_units * patient.insulin_sensitivity_factor * 0.2
        return total

    def _carbs_on_board(self, meals: list[tuple[int, float]], t: int, absorption_min: int) -> float:
        cob = 0.0
        for meal_t, carbs in meals:
            elapsed = t - meal_t
            if elapsed < 0:
                continue
            if elapsed >= absorption_min:
                continue
            remaining = 1 - (elapsed / absorption_min)
            cob += carbs * remaining
        return cob

    def _insulin_on_board(self, boluses: list[tuple[int, float]], t: int, action_min: int) -> float:
        iob = 0.0
        for bolus_t, units in boluses:
            elapsed = t - bolus_t
            if elapsed < 0:
                continue
            if elapsed >= action_min:
                continue
            remaining = 1 - (elapsed / action_min)
            iob += units * remaining
        return iob

    def _exercise_modifier(self, config: SimulationConfig, t: int) -> float:
        mod = 1.0
        for ex in config.exercise:
            if ex.start_min <= t <= ex.end_min:
                mod += 0.2 + (0.8 * ex.intensity)
        return mod

    def _summarize(self, points: list[dict], hypo_events: int, hyper_events: int) -> dict:
        values = [p["glucose_mgdl"] for p in points]
        in_range = [v for v in values if 70 <= v <= 180]
        return {
            "average_glucose": round(sum(values) / len(values), 2),
            "peak_glucose": round(max(values), 2),
            "minimum_glucose": round(min(values), 2),
            "time_in_range_percent": round((len(in_range) / len(values)) * 100, 2),
            "hypo_events": hypo_events,
            "hyper_events": hyper_events,
        }
