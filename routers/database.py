from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db  # type: ignore
from DATABASE import crud, schemas  # type: ignore
from api_schema import GetAllIndexResponse, GetIndexStatusResponse, IndexStatusDict  # type: ignore

router = APIRouter(dependencies=[Depends(get_db)], tags=["DATABASE"])


@router.post("/create_index")
def create_index(index: schemas.IndexCreate, db: Session = Depends(get_db)):
    db_index = crud.create_index(db, index)
    return db_index


@router.get("/get_index_status/{index_id}", response_model=GetIndexStatusResponse)
def get_index_status(index_id: str, db: Session = Depends(get_db)):
    try:
        status = crud.get_index_status(db, index_id)
        return GetIndexStatusResponse(
            data=status, status_name=IndexStatusDict[status], error=None
        )
    except Exception as e:
        return GetIndexStatusResponse(data=None, status_name=None, error=str(e))


@router.get("/get_all_index", response_model=GetAllIndexResponse)
def get_all_index(db: Session = Depends(get_db)):
    try:
        indexes = crud.get_all_index(db)
        return GetAllIndexResponse(data=indexes, error=None)
    except Exception as e:
        return GetAllIndexResponse(data=None, error=str(e))
