from pathlib import Path
from uuid import uuid4
from ..storage.json_store import JsonStore


class Repository:
    def __init__(self, file_name: str):
        base = Path(__file__).resolve().parents[1] / "data"
        self.store = JsonStore(base / file_name)

    def list(self):
        return self.store.all()

    def get(self, obj_id: str):
        return self.store.get(obj_id)

    def create(self, payload: dict):
        payload["id"] = str(uuid4())
        return self.store.create(payload)

    def update(self, obj_id: str, payload: dict):
        payload["id"] = obj_id
        return self.store.update(obj_id, payload)

    def delete(self, obj_id: str):
        return self.store.delete(obj_id)
