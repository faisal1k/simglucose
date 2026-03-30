from .engines.physiological import PhysiologicalEngine
from .engines.simplified import SimplifiedEngine


class EngineRegistry:
    def __init__(self):
        self._engines = {
            "physiological-v2": PhysiologicalEngine(),
            "simplified-v1": SimplifiedEngine(),
        }

    def get(self, model_name: str):
        return self._engines.get(model_name, self._engines["physiological-v2"])

    def default(self):
        return self._engines["physiological-v2"]
