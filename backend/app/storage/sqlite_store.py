import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteStore:
    def __init__(self, db_path: Path, table_name: str):
        self.db_path = db_path
        self.table_name = table_name
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_table(self):
        with self._connect() as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            conn.commit()

    def all(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(f"SELECT payload FROM {self.table_name}").fetchall()
            return [json.loads(row[0]) for row in rows]

    def get(self, obj_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT payload FROM {self.table_name} WHERE id = ?", (obj_id,)
            ).fetchone()
            return json.loads(row[0]) if row else None

    def create(self, obj: dict[str, Any]) -> dict[str, Any]:
        with self._connect() as conn:
            conn.execute(
                f"INSERT OR REPLACE INTO {self.table_name}(id, payload) VALUES(?, ?)",
                (obj["id"], json.dumps(obj)),
            )
            conn.commit()
        return obj

    def update(self, obj_id: str, obj: dict[str, Any]) -> dict[str, Any] | None:
        if not self.get(obj_id):
            return None
        with self._connect() as conn:
            conn.execute(
                f"UPDATE {self.table_name} SET payload = ? WHERE id = ?",
                (json.dumps(obj), obj_id),
            )
            conn.commit()
        return obj

    def delete(self, obj_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (obj_id,))
            conn.commit()
            return cursor.rowcount > 0

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()
            return int(row[0])
