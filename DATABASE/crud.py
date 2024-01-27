from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional


def get_index_path(db: Session, index_id: str):
    return db.query(models.Index).filter(models.Index.index_id == index_id).first()


def create_index(db: Session, index: schemas.IndexCreate):
    db_index = models.Index(
        index_id=index.index_id,
        index_path=index.index_path,
        index_status=index.index_status,
    )
    db.add(db_index)
    db.commit()
    db.refresh(db_index)
    return db_index


def get_all_index(db: Session):
    return db.query(models.Index).all()


def delete_index(db: Session, index_id: str):
    db.query(models.Index).filter(models.Index.index_id == index_id).delete()
    db.commit()


def update_index_state(db: Session, index_id: str, index_status: int):
    db.query(models.Index).filter(models.Index.index_id == index_id).update(
        {models.Index.index_status: index_status}
    )
    db.commit()


def update_index(db: Session, index_id: str, index_path: str, index_status: int):
    db.query(models.Index).filter(models.Index.index_id == index_id).update(
        {models.Index.index_path: index_path, models.Index.index_status: index_status}
    )
    db.commit()


def check_path_exist(db: Session, index_path: str):
    return (
        True
        if db.query(models.Index).filter(models.Index.index_path == index_path).first()
        else False
    )


def get_index_status(db: Session, index_id: str):
    index = db.query(models.Index).filter(models.Index.index_id == index_id).first()
    if index is not None:
        return index.index_status
    else:
        return None


def get_indexed_indexes(db: Session):
    return db.query(models.Index).filter(models.Index.index_status == 0).all()


def check_index_exist(db: Session, index_id: str):
    return (
        True
        if db.query(models.Index).filter(models.Index.index_id == index_id).first()
        else False
    )
