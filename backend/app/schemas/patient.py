from pydantic import BaseModel, Field


class PatientBase(BaseModel):
    name: str = Field(min_length=1)
    body_weight_kg: float = Field(gt=20, lt=300)
    age_years: int = Field(gt=0, lt=120)
    baseline_glucose_mgdl: float = Field(gt=40, lt=400)
    insulin_sensitivity_factor: float = Field(gt=1, lt=300, description="mg/dL drop per unit")
    carb_ratio: float = Field(gt=1, lt=60, description="grams of carb per unit")
    basal_rate_u_per_hr: float = Field(ge=0, lt=10)
    insulin_action_duration_min: int = Field(gt=30, lt=600)
    carb_absorption_duration_min: int = Field(gt=15, lt=600)
    glucose_effectiveness: float = Field(ge=0, le=1, description="fraction toward baseline per hour")
    variability_noise_std: float = Field(ge=0, le=30, default=2)
    activity_sensitivity_modifier: float = Field(gt=0, le=3, default=1.0)


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    id: str
