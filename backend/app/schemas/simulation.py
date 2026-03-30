from pydantic import BaseModel
from .patient import Patient
from .scenario import Scenario


class SimulationRequest(BaseModel):
    patient_id: str | None = None
    scenario_id: str | None = None
    patient: Patient | None = None
    scenario: Scenario | None = None
    seed: int | None = None


class SimulationPoint(BaseModel):
    t_min: int
    glucose_mgdl: float
    insulin_on_board_u: float
    carbs_on_board_g: float
    basal_units_delivered: float
    bolus_units_delivered: float
    meal_carbs_ingested: float


class SimulationSummary(BaseModel):
    average_glucose: float
    peak_glucose: float
    minimum_glucose: float
    time_in_range_percent: float
    hypo_events: int
    hyper_events: int


class SimulationResult(BaseModel):
    id: str
    patient_name: str
    scenario_name: str
    points: list[SimulationPoint]
    summary: SimulationSummary
    model_version: str
