import pytest
from httpx import AsyncClient

from main import app
from database import init_db, engine
from sqlmodel import SQLModel


@pytest.fixture(autouse=True)
def prepare_db(tmp_path, monkeypatch):
    # Use a temporary SQLite file for tests
    db_file = tmp_path / "test_notes.db"
    # Monkeypatch database module attributes before import
    monkeypatch.setenv("TEST_DB_PATH", str(db_file))
    # rebuild schema on the engine
    SQLModel.metadata.create_all(engine)
    yield


@pytest.mark.asyncio
async def test_crud_notes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create
        r = await ac.post("/notes", json={"title": "T1", "content": "C1"})
        assert r.status_code == 201
        note = r.json()
        note_id = note["id"]

        # get
        r = await ac.get(f"/notes/{note_id}")
        assert r.status_code == 200
        assert r.json()["title"] == "T1"

        # list
        r = await ac.get("/notes")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

        # update
        r = await ac.put(f"/notes/{note_id}", json={"title": "T1-upd", "content": "C1-upd"})
        assert r.status_code == 200
        assert r.json()["title"] == "T1-upd"

        # delete
        r = await ac.delete(f"/notes/{note_id}")
        assert r.status_code == 204

        # get missing
        r = await ac.get(f"/notes/{note_id}")
        assert r.status_code == 404
