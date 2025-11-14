from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class NoteBase(SQLModel):
    title: str
    content: str


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime
