from fastapi import APIRouter, HTTPException
from ..schemas.scenario import Scenario, ScenarioCreate
from ..services.repository import Repository

router = APIRouter(prefix="/scenarios", tags=["scenarios"])
repo = Repository("scenarios.json")


@router.get("", response_model=list[Scenario])
def list_scenarios():
    return repo.list()


@router.post("", response_model=Scenario)
def create_scenario(payload: ScenarioCreate):
    return repo.create(payload.model_dump())


@router.put("/{scenario_id}", response_model=Scenario)
def update_scenario(scenario_id: str, payload: ScenarioCreate):
    updated = repo.update(scenario_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return updated


@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: str):
    if not repo.delete(scenario_id):
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "deleted"}
