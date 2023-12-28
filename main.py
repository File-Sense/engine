import uvicorn
from re import sub
from os import path
from sys import argv
from typing import Dict
from fastapi import FastAPI
from settings import Settings  # type: ignore
from os import name as os_name
from AI.engine import AIEngine  # type: ignore
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from VECTORSTORE.vectorstore import VectorStore  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from routers import aiengine, database, vectorstore, common  # type: ignore
from api_schema import (  # type: ignore
    TaskData,
)

global reload_state
if "dev" not in argv:
    import ensure_exit  # type: ignore

    reload_state = False
else:
    reload_state = True

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ai_engine = AIEngine()
    app.state.vectorstore = VectorStore()
    yield
    app.state.ai_engine.release_models()


app = FastAPI(
    docs_url=None,
    lifespan=lifespan,
    redoc_url=None,
)
static_dir = path.join(settings.ROOT_DIR, "static")
if os_name == "nt":
    static_dir = sub(r"\\\\\?\\", "", static_dir)
    static_dir = static_dir.replace("\\", "/")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(aiengine.router, prefix="/api/aiengine")
app.include_router(database.router, prefix="/api/database")
app.include_router(vectorstore.router, prefix="/api/vectorstore")
app.include_router(common.router, prefix="/api/common")

task_state: Dict[str, TaskData] = {}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="File Sense AI API",
        description="This API Handles all the utilities required for file sense app",
        version="0.0.1",
        contact={"name": "Pasindu Akalpa", "email": "pasinduakalpa1998@gmail.com"},
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


# def list_image_paths(directory):
#     image_extensions = [".png", ".jpg", ".jpeg", ".ppm", ".gif", ".tiff", ".bmp"]
#     image_paths = []

#     try:
#         for root, _, files in walk(directory):
#             for file in files:
#                 if any(file.lower().endswith(ext) for ext in image_extensions):
#                     image_paths.append(path.normpath(path.join(root, file)))

#     except OSError as e:
#         print(f"Error reading directory '{directory}': {e}")

#     return image_paths


# def create_index_task(ai_engine: AIEngine, task_id: str, folder_path: str):
#     try:
#         image_paths = list_image_paths(folder_path)
#         image_embeddings = [
#             ai_engine.generate_image_embedding(image) for image in image_paths
#         ]
#         caption_embeddings = ai_engine.generate_text_embedding(
#             [ai_engine.generate_caption(image) for image in image_paths]
#         )
#         task_data = TaskData(
#             status="completed",
#             caption_embeddings=caption_embeddings,
#             image_embeddings=image_embeddings,
#             file_paths=image_paths,
#             folder_path=folder_path,
#             error=None,
#         )
#         task_state[task_id] = task_data
#     except Exception as e:
#         task_state[task_id] = TaskData(
#             status="failed",
#             caption_embeddings=None,
#             image_embeddings=None,
#             folder_path=folder_path,
#             file_paths=None,
#             error=str(e),
#         )
#         raise e


@app.get("/api/ping")
async def ping():
    return {"ping": "pong"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/favicon.ico")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="File Sense AI API",
        swagger_favicon_url="/static/icon192.png",
    )


# @app.post("/api/create_indexing_task", response_model=CreateIndexingTaskResponse)
# async def create_indexing_task(
#     r: Request, request: CreateIndexingTaskRequest, background_tasks: BackgroundTasks
# ):
#     try:
#         task_id = str(uuid4())
#         task_state[task_id] = TaskData(
#             status="running",
#             caption_embeddings=None,
#             file_paths=None,
#             image_embeddings=None,
#             folder_path=request.folder_path,
#             error=None,
#         )
#         background_tasks.add_task(
#             create_index_task, r.app.state.ai_engine, task_id, request.folder_path
#         )
#         return CreateIndexingTaskResponse(task_id=task_id, error=None)
#     except Exception as e:
#         return CreateIndexingTaskResponse(task_id=None, error=str(e))


# @app.get(
#     "/api/get_indexing_task_status_or_result/{task_id}",
# )
# async def get_indexing_task_status(task_id: str):
#     try:
#         if task_id not in task_state.keys():
#             raise Exception(f"Task with id '{task_id}' not found")
#         response = GetIndexingTaskResponse(
#             task_id=task_id,
#             data=task_state[task_id].model_dump(),
#             error=None,
#             status=task_state[task_id].status,
#         )
#         del task_state[task_id]
#         return response
#     except Exception as e:
#         return GetIndexingTaskResponse(
#             task_id=task_id, data=None, error=str(e), status="failed"
#         )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=reload_state)
