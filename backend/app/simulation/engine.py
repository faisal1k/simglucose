from .registry import EngineRegistry


class SimulationEngine:
    """Compatibility wrapper to preserve existing imports while supporting pluggable engines."""

    def __init__(self, model_name: str = "physiological-v2"):
        self.registry = EngineRegistry()
        self.engine = self.registry.get(model_name)
        self.model_version = self.engine.model_version

    def run(self, patient, config, seed=None):
        return self.engine.run(patient, config, seed)
