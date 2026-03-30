#!/usr/bin/env bash
set -euo pipefail
python -m compileall backend/app
python - <<'PY'
from backend.app.simulation.engine import SimulationEngine
from backend.app.simulation.models import PatientProfile, SimulationConfig, MealEvent, InsulinEvent
patient = PatientProfile(name='Smoke', body_weight_kg=70, age_years=30, baseline_glucose_mgdl=110, insulin_sensitivity_factor=40, carb_ratio=10, basal_rate_u_per_hr=1, insulin_action_duration_min=240, carb_absorption_duration_min=180, glucose_effectiveness=0.2)
config = SimulationConfig(duration_min=120, time_step_min=5, starting_glucose_mgdl=110, target_glucose_mgdl=110, meals=[MealEvent(time_min=10, carbs_g=40)], boluses=[InsulinEvent(time_min=5, units=4)])
result = SimulationEngine().run(patient, config, seed=1)
print(result.model_version, len(result.points))
PY
