from re import sub
from pathlib import Path
from os import path, name as os_name, mkdir
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

filesense_path = path.join(Path.home(), ".filesense")
if not path.exists(filesense_path):
    mkdir(filesense_path)

db_dir = path.join(filesense_path, "refdb.sqlite3")
if os_name == "nt":
    db_dir = sub(r"\\\\\?\\", "", db_dir)
    db_dir = db_dir.replace("\\", "/")

SQLALCHEMY_DATABASE_URL = "sqlite:///" + db_dir

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
