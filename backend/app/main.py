from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.db import get_connection


@asynccontextmanager
async def lifespan(_app: FastAPI):
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS items "
            "(id SERIAL PRIMARY KEY, name TEXT NOT NULL)"
        )
        conn.commit()
    yield


app = FastAPI(title="math-utils 全栈 Demo 后端", lifespan=lifespan)


class Item(BaseModel):
    name: str


@app.get("/api/health")
def health() -> dict:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
            db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok", "db": db_ok}


@app.get("/api/items")
def list_items() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id").fetchall()
    return [{"id": r[0], "name": r[1]} for r in rows]


@app.post("/api/items", status_code=201)
def create_item(item: Item) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id, name",
            (item.name,),
        ).fetchone()
        conn.commit()
    return {"id": row[0], "name": row[1]}
