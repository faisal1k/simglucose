from abc import ABC, abstractmethod
from .models import PatientProfile, SimulationConfig, SimulationResult


class SimulationEngineBase(ABC):
    model_version: str

    @abstractmethod
    def run(self, patient: PatientProfile, config: SimulationConfig, seed: int | None = None) -> SimulationResult:
        raise NotImplementedError
