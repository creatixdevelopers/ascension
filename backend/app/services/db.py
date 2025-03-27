from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

engine: Engine | None = None
session: sessionmaker[Session] | None = None

database_uri = settings.DATABASE_URI
if database_uri.startswith("postgres://"):
    engine = create_engine(database_uri)
    session = sessionmaker(engine)
elif database_uri.startswith("sqlite://"):
    engine = create_engine(database_uri, connect_args={"check_same_thread": False})
    session = sessionmaker(engine, expire_on_commit=False)
else:
    raise ValueError("Unsupported database type")


async def get_db() -> Generator[Session, None]:
    db: Session = session()
    try:
        yield db
    finally:
        db.close()


dbDep = Annotated[Session, Depends(get_db)]
