import os
from pathlib import Path
from uuid import uuid4
from ..storage.json_store import JsonStore
from ..storage.sqlite_store import SQLiteStore


class Repository:
    def __init__(self, file_name: str):
        base = Path(__file__).resolve().parents[1] / "data"
        table_name = file_name.replace(".json", "")

        self.json_store = JsonStore(base / file_name)
        self.sqlite_store = SQLiteStore(base / "app.db", table_name)
        self.store = self.sqlite_store if os.getenv("APP_STORAGE_BACKEND", "sqlite") == "sqlite" else self.json_store

        self._bootstrap_from_json_if_empty()

    def _bootstrap_from_json_if_empty(self) -> None:
        if self.store is not self.sqlite_store:
            return
        if self.sqlite_store.count() > 0:
            return
        for item in self.json_store.all():
            self.sqlite_store.create(item)

    def list(self):
        return self.store.all()

    def get(self, obj_id: str):
        return self.store.get(obj_id)

    def create(self, payload: dict):
        payload["id"] = payload.get("id") or str(uuid4())
        return self.store.create(payload)

    def update(self, obj_id: str, payload: dict):
        payload["id"] = obj_id
        return self.store.update(obj_id, payload)

    def delete(self, obj_id: str):
        return self.store.delete(obj_id)
