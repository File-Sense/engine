from os import path, walk
from fastapi import FastAPI, BackgroundTasks
import uvicorn
from settings import Settings
from uuid import uuid4
from sys import argv
from AI.engine import AIEngine
from typing import Dict
from model import *

global reload_state
if "dev" not in argv:
    import ensure_exit

    reload_state = False
else:
    reload_state = True

settings = Settings()
ai_engine = AIEngine()

app = FastAPI()

task_state: Dict[str, TaskData] = {}


def list_image_paths(directory):
    image_extensions = [".png", ".jpg", ".jpeg", ".ppm", ".gif", ".tiff", ".bmp"]
    image_paths = []

    try:
        for root, _, files in walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_paths.append(path.normpath(path.join(root, file)))

    except OSError as e:
        print(f"Error reading directory '{directory}': {e}")

    return image_paths


def create_index_task(task_id: str, folder_path: str):
    try:
        image_paths = list_image_paths(folder_path)
        image_embeddings = [
            ai_engine.generate_image_embedding(image) for image in image_paths
        ]
        caption_embeddings = ai_engine.generate_text_embedding(
            [ai_engine.generate_caption(image) for image in image_paths]
        )
        task_data = TaskData(
            status="completed",
            caption_embeddings=caption_embeddings,
            image_embeddings=image_embeddings,
            file_paths=image_paths,
            folder_path=folder_path,
            error=None,
        )
        task_state[task_id] = task_data
    except Exception as e:
        task_state[task_id] = TaskData(
            status="failed",
            caption_embeddings=None,
            image_embeddings=None,
            folder_path=folder_path,
            file_paths=None,
            error=str(e),
        )
        raise e


@app.get("/api/ping")
async def ping():
    return {"ping": "pong"}


@app.post("/api/get_text_embeddings", response_model=GetTextEmbeddingsResponse)
async def get_text_embeddings(request: GetTextEmbeddingsRequest):
    try:
        embeddings = ai_engine.generate_text_embedding(request.text)
        return GetTextEmbeddingsResponse(embeddings=embeddings, error=None)
    except Exception as e:
        return GetTextEmbeddingsResponse(embeddings=None, error=str(e))


@app.post("/api/get_image_embeddings", response_model=GetImageEmbeddingsResponse)
async def get_image_embeddings(request: GetImageEmbeddingsRequest):
    try:
        img_emb_list = [
            ai_engine.generate_image_embedding(image_path=img_path)
            for img_path in request.image_paths
        ]
        return GetImageEmbeddingsResponse(embeddings=img_emb_list, error=None)
    except Exception as e:
        return GetImageEmbeddingsResponse(embeddings=None, error=str(e))


@app.post("/api/get_image_caption", response_model=GetImageCaptionResponse)
async def get_image_caption(request: GetImageCaptionRequest):
    try:
        img_cap_list = [
            ai_engine.generate_caption(image_path=img_path)
            for img_path in request.image_path
        ]
        return GetImageCaptionResponse(caption=img_cap_list, error=None)
    except Exception as e:
        return GetImageCaptionResponse(caption=None, error=str(e))


@app.post(
    "/api/get_caption_with_embeddings", response_model=GetCaptionWithEmbeddingsResponse
)
async def get_caption_with_embeddings(request: GetCaptionWithEmbeddingsRequest):
    try:
        img_cap_list = [
            ai_engine.generate_caption(image_path=img_path)
            for img_path in request.image_paths
        ]
        cap_text_emb_list = ai_engine.generate_text_embedding(img_cap_list)
        img_emb_list = [
            ai_engine.generate_image_embedding(image_path=img_path)
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


@app.post("/api/create_indexing_task", response_model=CreateIndexingTaskResponse)
async def create_indexing_task(
    request: CreateIndexingTaskRequest, background_tasks: BackgroundTasks
):
    try:
        task_id = str(uuid4())
        task_state[task_id] = TaskData(
            status="running",
            caption_embeddings=None,
            file_paths=None,
            image_embeddings=None,
            folder_path=request.folder_path,
            error=None,
        )
        background_tasks.add_task(create_index_task, task_id, request.folder_path)
        return CreateIndexingTaskResponse(task_id=task_id, error=None)
    except Exception as e:
        return CreateIndexingTaskResponse(task_id=None, error=str(e))


@app.get(
    "/api/get_indexing_task_status_or_result/{task_id}",
)
async def get_indexing_task_status(task_id: str):
    try:
        if task_id not in task_state.keys():
            raise Exception(f"Task with id '{task_id}' not found")
        response = GetIndexingTaskResponse(
            task_id=task_id,
            data=task_state[task_id].model_dump(),
            error=None,
            status=task_state[task_id].status,
        )
        del task_state[task_id]
        return response
    except Exception as e:
        return GetIndexingTaskResponse(
            task_id=task_id, data=None, error=str(e), status="failed"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=reload_state)
