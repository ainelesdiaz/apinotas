from sqlmodel import create_engine, SQLModel

sqlite_file_name = "notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
