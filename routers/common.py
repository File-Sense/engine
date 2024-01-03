from io import BytesIO
from os import path, walk
from fastapi import (
    APIRouter,
    Depends,
    Request,
    BackgroundTasks,
    File,
    UploadFile,
    HTTPException,
    status as HTTPStatus,
)
from sqlalchemy.orm import Session
from dependencies import get_db  # type: ignore
from DATABASE import crud, schemas  # type: ignore
from api_schema import (  # type: ignore
    BaseSearchResultResponse,
    DeleteIndexRequest,
    DeleteIndexResponse,
    IndexDirRequest,
    IndexDirResponse,
    SearchByImageRequest,
    SearchByTextRequest,
)
from checksumdir import dirhash

from AI.engine import AIEngine  # type: ignore
from VECTORSTORE.vectorstore import VectorStore  # type: ignore

router = APIRouter(dependencies=[Depends(get_db)], tags=["COMMON"])


def list_image_path(directory: str):
    image_extensions = [".png", ".jpg", ".jpeg", ".ppm", ".gif", ".tiff", ".bmp"]
    image_paths = []
    try:
        for root, _, files in walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in image_extensions):
                    image_paths.append(path.join(root, file))
    except Exception as e:
        raise e
    return image_paths


def create_index(
    directory: str,
    db: Session,
    vs: VectorStore,
    ae: AIEngine,
    collection_name: str,
):
    try:
        img_path_list = list_image_path(directory)
        id_list = [str(hash(img_path)) for img_path in img_path_list]
        caption_list = [ae.generate_caption(img_path) for img_path in img_path_list]
        caption_emb_list = ae.generate_text_embedding(caption_list)
        images_emb_list = [
            ae.generate_image_embedding(img_path) for img_path in img_path_list
        ]
        metadata_list = [{"path": img_path} for img_path in img_path_list]
        vs.upsert_to_collections(
            id_list,
            caption_list,
            caption_emb_list,
            images_emb_list,
            metadata_list,
            collection_name,
        )
        crud.update_index_state(db, collection_name, 0)
    except Exception as e:
        print(e)
        crud.update_index_status(db, collection_name, -1)
        raise e


@router.post(
    "/index_directory",
    response_model=IndexDirResponse,
)
def index_directory(
    request: IndexDirRequest,
    r: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not path.isdir(request.dir_path):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_404_NOT_FOUND,
            detail=IndexDirResponse(
                index_id=None, error="Invalid directory path"
            ).model_dump(),
        )
    if crud.check_path_exist(db, request.dir_path):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_404_NOT_FOUND,
            detail=IndexDirResponse(
                index_id=None, error="Path already indexed"
            ).model_dump(),
        )
    try:
        collection_name = dirhash(request.dir_path)
        crud.create_index(
            db,
            schemas.IndexCreate(
                index_id=collection_name,
                index_path=request.dir_path,
                index_status=1,
            ),
        )
        background_tasks.add_task(
            create_index,
            request.dir_path,
            db,
            r.app.state.vectorstore,
            r.app.state.ai_engine,
            collection_name,
        )
        return IndexDirResponse(index_id=collection_name, error=None)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=IndexDirResponse(index_id=None, error=str(e)).model_dump(),
        )


@router.get("/search_by_text", response_model=BaseSearchResultResponse)
def search_by_text(
    r: Request,
    request: SearchByTextRequest = Depends(),
    db: Session = Depends(get_db),
):
    if not crud.check_index_exist(db, request.index_name):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_404_NOT_FOUND,
            detail=BaseSearchResultResponse(
                data=None, error="Index does not exist"
            ).model_dump(),
        )
    try:
        text_emb = r.app.state.ai_engine.generate_text_embedding(
            [request.search_string]
        )
        result = r.app.state.vectorstore.search_by_text(
            text_emb, request.index_name, request.limit
        )
        return BaseSearchResultResponse(data=result, error=None)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=IndexDirResponse(index_id=None, error=str(e)).model_dump(),
        )


@router.post("/search_by_image", response_model=BaseSearchResultResponse)
def search_by_image(
    r: Request,
    request: SearchByImageRequest = Depends(),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not crud.check_index_exist(db, request.index_name):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_404_NOT_FOUND,
            detail=BaseSearchResultResponse(
                data=None, error="Index does not exist"
            ).model_dump(),
        )
    try:
        image_bytes = BytesIO(image.file.read())
        image_emb = r.app.state.ai_engine.generate_image_embedding(
            "", image=image_bytes
        )
        result = r.app.state.vectorstore.search_by_image(
            image_emb, request.index_name, request.limit
        )
        return BaseSearchResultResponse(data=result, error=None)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=IndexDirResponse(index_id=None, error=str(e)).model_dump(),
        )


@router.delete("/delete_index", response_model=DeleteIndexResponse)
def delete_index(
    r: Request,
    request: DeleteIndexRequest = Depends(),
    db: Session = Depends(get_db),
):
    if not crud.check_index_exist(db, request.index_name):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_404_NOT_FOUND,
            detail=BaseSearchResultResponse(
                data=None, error="Index does not exist"
            ).model_dump(),
        )
    try:
        crud.delete_index(db, request.index_name)
        r.app.state.vectorstore.delete_collection(request.index_name)
        return DeleteIndexResponse(data="OK", error=None)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=IndexDirResponse(index_id=None, error=str(e)).model_dump(),
        )
