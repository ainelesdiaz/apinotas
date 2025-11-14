from fastapi import FastAPI, HTTPException
from typing import List
from sqlmodel import Session, select

from database import engine, init_db
from models import Note, NoteCreate, NoteRead

app = FastAPI(title="API de Notas")


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/notes", response_model=NoteRead, status_code=201)
def create_note(note_in: NoteCreate):
    with Session(engine) as session:
        note = Note.from_orm(note_in)
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


@app.get("/notes", response_model=List[NoteRead])
def list_notes():
    with Session(engine) as session:
        notes = session.exec(select(Note).order_by(Note.id)).all()
        return notes


@app.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return note


@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note_in: NoteCreate):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        note.title = note_in.title
        note.content = note_in.content
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        session.delete(note)
        session.commit()
        return None
