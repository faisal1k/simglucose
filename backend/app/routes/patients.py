from fastapi import APIRouter, HTTPException
from ..schemas.patient import Patient, PatientCreate, PatientUpdate
from ..services.repository import Repository

router = APIRouter(prefix="/patients", tags=["patients"])
repo = Repository("patients.json")


@router.get("", response_model=list[Patient])
def list_patients():
    return repo.list()


@router.post("", response_model=Patient)
def create_patient(payload: PatientCreate):
    return repo.create(payload.model_dump())


@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, payload: PatientUpdate):
    updated = repo.update(patient_id, payload.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated


@router.delete("/{patient_id}")
def delete_patient(patient_id: str):
    if not repo.delete(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "deleted"}
