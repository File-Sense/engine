from sqlalchemy import Column, Integer, String
from .database import Base


class Index(Base):
    __tablename__ = "index"

    id = Column(Integer, primary_key=True, index=True)
    index_id = Column(String, unique=True, index=True)
    index_path = Column(String, unique=True, index=True)
    index_status = Column(Integer, index=True)
