from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import patients, scenarios, simulation

app = FastAPI(title="Virtual Glucose Lab API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(scenarios.router)
app.include_router(simulation.router)


@app.get("/health")
def health():
    return {"status": "ok"}
