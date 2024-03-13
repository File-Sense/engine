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
from VECTORSTORE.vectorstore import VectorStore  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from routers import aiengine, database, vectorstore, common  # type: ignore
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
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
        description="This API Handles all the AI utilities required for file sense app",
        version="0.1.1",
        contact={"name": "Pasindu Akalpa", "email": "pasinduakalpa1998@gmail.com"},
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.get("/api/ping", tags=["DEFAULT"])
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=270, reload=reload_state)
