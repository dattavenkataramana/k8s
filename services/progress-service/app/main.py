import os
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATABASE_PATH = os.getenv(
    "DATABASE_PATH", str(Path(__file__).resolve().parent.parent / "progress.db")
)


class ProgressUpdate(BaseModel):
    completed: bool


class ProgressRecord(BaseModel):
    lab_id: int = Field(gt=0)
    completed: bool
    updated_at: str


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with closing(get_connection()) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                lab_id INTEGER PRIMARY KEY,
                completed INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


app = FastAPI(
    title="Progress Service",
    version="1.0.0",
    description="Owns learner progress data.",
)


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with closing(get_connection()) as connection:
            connection.execute("SELECT 1")
        return {"status": "healthy", "service": "progress-service"}
    except sqlite3.Error as error:
        raise HTTPException(status_code=503, detail="Database unavailable") from error


@app.get("/api/v1/info")
def info() -> dict[str, str]:
    return {"name": "progress-service", "version": "1.0.0"}


@app.get("/api/v1/progress", response_model=list[ProgressRecord])
def list_progress() -> list[ProgressRecord]:
    with closing(get_connection()) as connection:
        rows = connection.execute(
            "SELECT lab_id, completed, updated_at FROM progress ORDER BY lab_id"
        ).fetchall()
    return [
        ProgressRecord(
            lab_id=row["lab_id"],
            completed=bool(row["completed"]),
            updated_at=row["updated_at"],
        )
        for row in rows
    ]


@app.put("/api/v1/progress/{lab_id}", response_model=ProgressRecord)
def update_progress(lab_id: int, payload: ProgressUpdate) -> ProgressRecord:
    if lab_id < 1:
        raise HTTPException(status_code=422, detail="lab_id must be positive")
    updated_at = datetime.now(UTC).isoformat()
    with closing(get_connection()) as connection:
        connection.execute(
            """
            INSERT INTO progress (lab_id, completed, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(lab_id) DO UPDATE SET
                completed = excluded.completed,
                updated_at = excluded.updated_at
            """,
            (lab_id, int(payload.completed), updated_at),
        )
        connection.commit()
    return ProgressRecord(
        lab_id=lab_id, completed=payload.completed, updated_at=updated_at
    )

