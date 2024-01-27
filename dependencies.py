from DATABASE import models  # type: ignore
from DATABASE.database import SessionLocal, engine  # type: ignore

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
