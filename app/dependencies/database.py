from database.database import SessionLocal
from sqlalchemy import text


def get_db():
    db = SessionLocal()
    db.execute(text("PRAGMA foreign_keys = true;"))
    try:
        yield db
    finally:
        db.close
