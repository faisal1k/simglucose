# Virtual Glucose Lab (Full-Stack MVP)

A polished, simulation-based web app inspired by simglucose for creating and testing custom virtual diabetes patients.

## Project Structure

- `backend/` — FastAPI API + simulation engine + JSON persistence
- `frontend/` — React + TypeScript + Tailwind + Recharts dashboard UI

## Features Implemented

- Custom patient profile CRUD (`/patients`)
- Scenario CRUD (`/scenarios`)
- Simulation execution (`/simulate`)
- Saved simulation retrieval (`/simulation/{id}`)
- Simplified modular glucose-insulin model with configurable physiology
- Editable patient physiology and behavior settings
- Meal and bolus timeline editors
- Interactive glucose chart + run summary cards
- Comparison mode (second run overlay)
- Clone patient workflow
- Sample patients and sample scenarios preloaded

## Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Frontend Setup (React + TS + Tailwind)

```bash
cd frontend
npm install
npm run dev
```

Frontend app:
- `http://127.0.0.1:5173`

## How the Simulation Engine Works (Current Version)

Code location:
- Core logic: `backend/app/simulation/engine.py`
- Domain models: `backend/app/simulation/models.py`

Current `simplified-v1` behavior:
1. Simulates in fixed `time_step_min` increments.
2. Applies carbohydrate absorption via a smooth bell-shaped curve over `carb_absorption_duration_min`.
3. Applies insulin action via bell-shaped decay over `insulin_action_duration_min`.
4. Adds basal insulin each step; optional correction insulin is auto-added above threshold.
5. Pulls glucose toward `baseline_glucose_mgdl` using `glucose_effectiveness`.
6. Applies optional exercise sensitivity boost and noise/disturbance.
7. Produces time-series points and summary metrics:
   - average / peak / minimum glucose
   - time in range (70–180 mg/dL)
   - hypo and hyper event counts

## How to Define Your Own Patients

Use either:
- UI: **Patients** page → create/edit fields and save.
- API: `POST /patients` with physiology fields.

Patient fields are validated with Pydantic in:
- `backend/app/schemas/patient.py`

Storage is JSON-based in:
- `backend/app/data/patients.json`

## How to Swap in Real simglucose Logic Later

The architecture isolates simulation concerns behind:
- `SimulationEngine.run(...)` in `backend/app/simulation/engine.py`
- simulation DTO/domain models in `backend/app/simulation/models.py`

To upgrade:
1. Replace internals of `SimulationEngine` with richer physiological equations.
2. Keep `SimulationConfig` and output shape stable to avoid breaking frontend/API.
3. Optionally add new physiology fields in `schemas/patient.py` and pass-through mappings in `routes/simulation.py`.
4. Version model behavior using `model_version` in simulation results.

## Useful API Endpoints

- `GET /patients`
- `POST /patients`
- `PUT /patients/{id}`
- `DELETE /patients/{id}`
- `GET /scenarios`
- `POST /scenarios`
- `PUT /scenarios/{id}`
- `DELETE /scenarios/{id}`
- `POST /simulate`
- `GET /simulation/{id}`

## Example simulate payload

```json
{
  "patient_id": "sample-patient-1",
  "scenario_id": "sample-scenario-1",
  "seed": 7
}
```

## Notes

- This MVP prioritizes extensible architecture and end-to-end usability over clinical fidelity.
- JSON storage keeps local iteration simple; swapping to SQLite is straightforward by replacing `JsonStore` and repository wiring.
