from api_schema import (  # type: ignore
    GetCaptionWithEmbeddingsRequest,
    GetCaptionWithEmbeddingsResponse,
    GetImageCaptionRequest,
    GetImageCaptionResponse,
    GetImageEmbeddingsRequest,
    GetImageEmbeddingsResponse,
    GetTextEmbeddingsRequest,
    GetTextEmbeddingsResponse,
)
from fastapi import APIRouter, Request

router = APIRouter(tags=["AI ENGINE"])


@router.post("/get_text_embeddings", response_model=GetTextEmbeddingsResponse)
async def get_text_embeddings(r: Request, request: GetTextEmbeddingsRequest):
    try:
        embeddings = r.app.state.ai_engine.generate_text_embedding(request.text)
        return GetTextEmbeddingsResponse(embeddings=embeddings, error=None)
    except Exception as e:
        return GetTextEmbeddingsResponse(embeddings=None, error=str(e))


@router.post(
    "/get_image_embeddings",
    response_model=GetImageEmbeddingsResponse,
)
async def get_image_embeddings(r: Request, request: GetImageEmbeddingsRequest):
    try:
        img_emb_list = [
            r.app.state.ai_engine.generate_image_embedding(image_path=img_path)
            for img_path in request.image_paths
        ]
        return GetImageEmbeddingsResponse(embeddings=img_emb_list, error=None)
    except Exception as e:
        return GetImageEmbeddingsResponse(embeddings=None, error=str(e))


@router.post("/get_image_caption", response_model=GetImageCaptionResponse)
async def get_image_caption(r: Request, request: GetImageCaptionRequest):
    try:
        img_cap_list = [
            r.app.state.ai_engine.generate_caption(image_path=img_path)
            for img_path in request.image_path
        ]
        return GetImageCaptionResponse(caption=img_cap_list, error=None)
    except Exception as e:
        return GetImageCaptionResponse(caption=None, error=str(e))


@router.post(
    "/get_caption_with_embeddings",
    response_model=GetCaptionWithEmbeddingsResponse,
)
async def get_caption_with_embeddings(
    r: Request, request: GetCaptionWithEmbeddingsRequest
):
    try:
        img_cap_list = [
            r.app.state.ai_engine.generate_caption(image_path=img_path)
            for img_path in request.image_paths
        ]
        cap_text_emb_list = r.app.state.ai_engine.generate_text_embedding(img_cap_list)
        img_emb_list = [
            r.app.state.ai_engine.generate_image_embedding(image_path=img_path)
            for img_path in request.image_paths
        ]
        return GetCaptionWithEmbeddingsResponse(
            caption=img_cap_list,
            text_embeddings=cap_text_emb_list,
            image_embeddings=img_emb_list,
            error=None,
        )
    except Exception as e:
        return GetCaptionWithEmbeddingsResponse(
            caption=None, text_embeddings=None, image_embeddings=None, error=str(e)
        )
