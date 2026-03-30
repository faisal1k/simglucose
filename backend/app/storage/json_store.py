import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: list[dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def all(self) -> list[dict[str, Any]]:
        return self._read()

    def create(self, obj: dict[str, Any]) -> dict[str, Any]:
        data = self._read()
        data.append(obj)
        self._write(data)
        return obj

    def update(self, obj_id: str, obj: dict[str, Any]) -> dict[str, Any] | None:
        data = self._read()
        for i, item in enumerate(data):
            if item.get("id") == obj_id:
                data[i] = obj
                self._write(data)
                return obj
        return None

    def delete(self, obj_id: str) -> bool:
        data = self._read()
        filtered = [item for item in data if item.get("id") != obj_id]
        if len(filtered) == len(data):
            return False
        self._write(filtered)
        return True

    def get(self, obj_id: str) -> dict[str, Any] | None:
        return next((item for item in self._read() if item.get("id") == obj_id), None)
