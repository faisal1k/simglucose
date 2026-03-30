.PHONY: preflight setup-backend run-backend run-frontend smoke

preflight:
	./scripts/presentation_ready.sh

setup-backend:
	python -m venv backend/.venv
	. backend/.venv/bin/activate && pip install -r backend/requirements.txt

run-backend:
	. backend/.venv/bin/activate && uvicorn app.main:app --reload --port 8000 --app-dir backend

run-frontend:
	cd frontend && npm install && npm run dev

smoke:
	./scripts/smoke.sh
