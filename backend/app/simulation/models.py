from dataclasses import dataclass, field


@dataclass
class PatientProfile:
    name: str
    body_weight_kg: float
    age_years: int
    baseline_glucose_mgdl: float
    insulin_sensitivity_factor: float
    carb_ratio: float
    basal_rate_u_per_hr: float
    insulin_action_duration_min: int
    carb_absorption_duration_min: int
    glucose_effectiveness: float
    variability_noise_std: float = 2.0
    activity_sensitivity_modifier: float = 1.0


@dataclass
class SimulationEvent:
    time_min: int


@dataclass
class MealEvent(SimulationEvent):
    carbs_g: float


@dataclass
class InsulinEvent(SimulationEvent):
    units: float


@dataclass
class ExerciseEvent:
    start_min: int
    end_min: int
    intensity: float


@dataclass
class BasalProfile:
    units_per_hour: float


@dataclass
class SimulationConfig:
    duration_min: int
    time_step_min: int
    starting_glucose_mgdl: float
    target_glucose_mgdl: float
    meals: list[MealEvent] = field(default_factory=list)
    boluses: list[InsulinEvent] = field(default_factory=list)
    exercise: list[ExerciseEvent] = field(default_factory=list)
    disturbance_std: float = 0.0
    correction_threshold_mgdl: float | None = None
    model_name: str = "physiological-v2"
    controller_enabled: bool = True
    controller_kp: float = 0.015
    controller_ki: float = 0.00008
    controller_kd: float = 0.08
    activity_effect_scale: float = 1.0


@dataclass
class SimulationResult:
    points: list[dict]
    summary: dict
    model_version: str
