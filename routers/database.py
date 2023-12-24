from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db  # type: ignore
from DATABASE import crud, schemas  # type: ignore

router = APIRouter(
    dependencies=[Depends(get_db)],
)


@router.post("/create_index", tags=["DATABASE"])
def create_index(index: schemas.IndexCreate, db: Session = Depends(get_db)):
    db_index = crud.create_index(db, index)
    return db_index


@router.get("/get_index_status/{index_id}", tags=["DATABASE"])
def get_index_status(index_id: str, db: Session = Depends(get_db)):
    status = crud.get_index_status(db, index_id)
    return status.index_status
