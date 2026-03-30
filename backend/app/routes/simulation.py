from uuid import uuid4
from fastapi import APIRouter, HTTPException
from ..schemas.patient import Patient
from ..schemas.scenario import Scenario
from ..schemas.simulation import SimulationRequest, SimulationResult
from ..services.repository import Repository
from ..simulation.engine import SimulationEngine
from ..simulation.models import (
    ExerciseEvent,
    InsulinEvent,
    MealEvent,
    PatientProfile,
    SimulationConfig,
)

router = APIRouter(tags=["simulation"])
patient_repo = Repository("patients.json")
scenario_repo = Repository("scenarios.json")
sim_repo = Repository("simulations.json")
engine = SimulationEngine()


def _resolve_patient(payload: SimulationRequest) -> Patient:
    if payload.patient:
        return payload.patient
    if payload.patient_id:
        found = patient_repo.get(payload.patient_id)
        if not found:
            raise HTTPException(404, "Patient not found")
        return Patient(**found)
    raise HTTPException(400, "Provide either patient_id or patient")


def _resolve_scenario(payload: SimulationRequest) -> Scenario:
    if payload.scenario:
        return payload.scenario
    if payload.scenario_id:
        found = scenario_repo.get(payload.scenario_id)
        if not found:
            raise HTTPException(404, "Scenario not found")
        return Scenario(**found)
    raise HTTPException(400, "Provide either scenario_id or scenario")


@router.post("/simulate", response_model=SimulationResult)
def simulate(payload: SimulationRequest):
    patient = _resolve_patient(payload)
    scenario = _resolve_scenario(payload)

    result = engine.run(
        patient=PatientProfile(**patient.model_dump(exclude={"id"})),
        config=SimulationConfig(
            duration_min=scenario.duration_min,
            time_step_min=scenario.time_step_min,
            starting_glucose_mgdl=scenario.starting_glucose_mgdl,
            target_glucose_mgdl=scenario.target_glucose_mgdl,
            meals=[MealEvent(**m.model_dump()) for m in scenario.meals],
            boluses=[InsulinEvent(**b.model_dump()) for b in scenario.boluses],
            exercise=[ExerciseEvent(**e.model_dump()) for e in scenario.exercise],
            disturbance_std=scenario.disturbance_std,
            correction_threshold_mgdl=scenario.correction_threshold_mgdl,
        ),
        seed=payload.seed,
    )

    response = {
        "id": str(uuid4()),
        "patient_name": patient.name,
        "scenario_name": scenario.name,
        "points": result.points,
        "summary": result.summary,
        "model_version": result.model_version,
    }
    sim_repo.create(response.copy())
    return response


@router.get("/simulation/{simulation_id}", response_model=SimulationResult)
def get_simulation(simulation_id: str):
    found = sim_repo.get(simulation_id)
    if not found:
        raise HTTPException(404, "Simulation not found")
    return found
