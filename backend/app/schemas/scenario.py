from pydantic import BaseModel, Field


class MealEvent(BaseModel):
    time_min: int = Field(ge=0)
    carbs_g: float = Field(gt=0)


class InsulinEvent(BaseModel):
    time_min: int = Field(ge=0)
    units: float = Field(gt=0)


class ExerciseEvent(BaseModel):
    start_min: int = Field(ge=0)
    end_min: int = Field(gt=0)
    intensity: float = Field(gt=0, le=1)


class ScenarioBase(BaseModel):
    name: str
    duration_min: int = Field(gt=30, le=24 * 60)
    time_step_min: int = Field(gt=0, le=15, default=5)
    starting_glucose_mgdl: float = Field(gt=40, lt=500)
    target_glucose_mgdl: float = Field(gt=60, lt=180, default=110)
    meals: list[MealEvent] = []
    boluses: list[InsulinEvent] = []
    correction_threshold_mgdl: float | None = Field(default=None, gt=120, lt=350)
    exercise: list[ExerciseEvent] = []
    disturbance_std: float = Field(default=0, ge=0, le=30)

    # Optional tuning knobs. Backward-compatible defaults preserve existing payloads.
    model_name: str = Field(default="physiological-v2")
    controller_enabled: bool = Field(default=True)
    controller_kp: float = Field(default=0.015, ge=0, le=1)
    controller_ki: float = Field(default=0.00008, ge=0, le=1)
    controller_kd: float = Field(default=0.08, ge=0, le=2)
    activity_effect_scale: float = Field(default=1.0, ge=0, le=3)


class ScenarioCreate(ScenarioBase):
    pass


class Scenario(ScenarioBase):
    id: str
