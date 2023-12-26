from typing import Sequence
from chromadb import Collection
from fastapi import APIRouter, Request

router = APIRouter(tags=["VECTORSTORE"])


@router.get("/is_alive", response_model=int)
def is_alive(r: Request):
    return r.app.state.vectorstore.is_alive()


@router.get("/get_all_indexed", response_model=Sequence[Collection])
def get_all_indexed(r: Request):
    return r.app.state.vectorstore.get_list_collections()
