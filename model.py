from typing import List, Union
from pydantic import BaseModel


class GetTextEmbeddingsRequest(BaseModel):
    text: List[str]


class GetTextEmbeddingsResponse(BaseModel):
    embeddings: Union[List[List[float]], None]
    error: Union[str, None]


class GetImageEmbeddingsRequest(BaseModel):
    image_paths: List[str]


class GetImageEmbeddingsResponse(BaseModel):
    embeddings: Union[List[List[float]], None]
    error: Union[str, None]


class GetImageCaptionRequest(BaseModel):
    image_path: List[str]


class GetImageCaptionResponse(BaseModel):
    caption: Union[List[str], None]
    error: Union[str, None]


class GetCaptionWithEmbeddingsRequest(BaseModel):
    image_paths: List[str]


class GetCaptionWithEmbeddingsResponse(BaseModel):
    caption: Union[List[str], None]
    text_embeddings: Union[List[List[float]], None]
    image_embeddings: Union[List[List[float]], None]
    error: Union[str, None]


class CreateIndexingTaskRequest(BaseModel):
    folder_path: str


class CreateIndexingTaskResponse(BaseModel):
    task_id: Union[str, None]
    error: Union[str, None]


class GetIndexingTaskRequest(BaseModel):
    task_id: str


class TaskData(BaseModel):
    status: str
    caption_embeddings: Union[List[List[float]], None]
    image_embeddings: Union[List[List[float]], None]
    file_paths: Union[List[str], None]
    folder_path: str
    error: Union[str, None]


class GetIndexingTaskResponse(BaseModel):
    task_id: str
    status: str
    data: Union[TaskData, None]
    error: Union[str, None]
