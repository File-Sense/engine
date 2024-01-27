from re import sub
from settings import Settings  # type: ignore
from os import path, name as os_name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

settings = Settings()

db_dir = path.join(settings.ROOT_DIR, "DATABASE", "db", "refdb.sqlite3")
if os_name == "nt":
    db_dir = sub(r"\\\\\?\\", "", db_dir)
    db_dir = db_dir.replace("\\", "/")

SQLALCHEMY_DATABASE_URL = "sqlite:///" + db_dir

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
