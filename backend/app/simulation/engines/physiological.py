import random
from ...controller import PIDConfig, PIDController
from ..base import SimulationEngineBase
from ..models import BasalProfile, PatientProfile, SimulationConfig, SimulationResult


class PhysiologicalEngine(SimulationEngineBase):
    """Bergman-inspired minimal model with carb/insulin compartments and optional PID basal modulation."""

    model_version = "physiological-v2"

    def run(self, patient: PatientProfile, config: SimulationConfig, seed: int | None = None) -> SimulationResult:
        if seed is not None:
            random.seed(seed)

        dt = config.time_step_min
        dt_hr = dt / 60

        glucose = config.starting_glucose_mgdl
        insulin_effect_state = 0.0
        insulin_on_board = 0.0
        carbs_on_board = 0.0
        basal = BasalProfile(units_per_hour=patient.basal_rate_u_per_hr)

        meal_map = {m.time_min: m.carbs_g for m in config.meals}
        bolus_map = {b.time_min: b.units for b in config.boluses}

        pid = None
        if config.controller_enabled:
            pid = PIDController(
                PIDConfig(
                    kp=config.controller_kp,
                    ki=config.controller_ki,
                    kd=config.controller_kd,
                    target_glucose=config.target_glucose_mgdl,
                )
            )

        points: list[dict] = []
        hypo_events = hyper_events = 0
        in_hypo = in_hyper = False

        k_carb = 60 / max(patient.carb_absorption_duration_min, 1)
        k_insulin = 60 / max(patient.insulin_action_duration_min, 1)
        carb_to_glucose_gain = (patient.insulin_sensitivity_factor / patient.carb_ratio) * 0.9
        insulin_action_gain = 0.04

        for t in range(0, config.duration_min + dt, dt):
            meal_carbs_ingested = meal_map.get(t, 0.0)
            bolus_units = bolus_map.get(t, 0.0)

            controller_u_per_hr = pid.step(glucose, dt) if pid else 0.0
            basal_units = (basal.units_per_hour + controller_u_per_hr) * dt_hr

            if config.correction_threshold_mgdl and glucose > config.correction_threshold_mgdl:
                bolus_units += max(0.0, (glucose - config.target_glucose_mgdl) / patient.insulin_sensitivity_factor) * 0.2

            carbs_on_board += meal_carbs_ingested
            insulin_on_board += basal_units + bolus_units

            absorbed_carbs = carbs_on_board * k_carb * dt_hr
            carbs_on_board = max(0.0, carbs_on_board - absorbed_carbs)

            insulin_cleared = insulin_on_board * k_insulin * dt_hr
            insulin_on_board = max(0.0, insulin_on_board - insulin_cleared)

            insulin_effect_state += (insulin_action_gain * insulin_on_board - 0.25 * insulin_effect_state) * dt_hr

            exercise_multiplier = self._exercise_multiplier(config, t)
            noise = random.gauss(0, patient.variability_noise_std + config.disturbance_std)

            d_glucose = (
                -patient.glucose_effectiveness * (glucose - patient.baseline_glucose_mgdl)
                - patient.insulin_sensitivity_factor * insulin_effect_state * 0.01 * exercise_multiplier
                + carb_to_glucose_gain * absorbed_carbs
            ) * dt_hr

            glucose = max(35.0, min(500.0, glucose + d_glucose + noise))

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
                    "bolus_units_delivered": round(bolus_units, 3),
                    "meal_carbs_ingested": round(meal_carbs_ingested, 2),
                }
            )

        values = [p["glucose_mgdl"] for p in points]
        in_range = [v for v in values if 70 <= v <= 180]
        summary = {
            "average_glucose": round(sum(values) / len(values), 2),
            "peak_glucose": round(max(values), 2),
            "minimum_glucose": round(min(values), 2),
            "time_in_range_percent": round((len(in_range) / len(values)) * 100, 2),
            "hypo_events": hypo_events,
            "hyper_events": hyper_events,
        }
        return SimulationResult(points=points, summary=summary, model_version=self.model_version)

    def _exercise_multiplier(self, config: SimulationConfig, t: int) -> float:
        multiplier = 1.0
        for ex in config.exercise:
            if ex.start_min <= t <= ex.end_min:
                multiplier += ex.intensity * config.activity_effect_scale
        return multiplier
