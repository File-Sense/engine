from typing import Sequence
from chromadb import Collection
from fastapi import APIRouter, Request, HTTPException, status as HTTPStatus

router = APIRouter(tags=["VECTORSTORE"])


@router.get("/is_alive", response_model=int)
def is_alive(r: Request):
    try:
        return r.app.state.vectorstore.is_alive()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get_all_indexed", response_model=Sequence[Collection])
def get_all_indexed(r: Request):
    try:
        return r.app.state.vectorstore.get_list_collections()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
