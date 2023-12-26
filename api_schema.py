from typing import List, Optional
from pydantic import BaseModel

from DATABASE.schemas import Index  # type: ignore

IndexStatusDict = {
    -1: "FAILED",
    0: "INDEXED",
    1: "INDEXING",
}


class BaseResponse(BaseModel):
    error: Optional[str]


class BaseSearchRequest(BaseModel):
    index_name: str
    limit: int = 3


class GetTextEmbeddingsRequest(BaseModel):
    text: List[str]


class GetTextEmbeddingsResponse(BaseResponse):
    embeddings: Optional[List[List[float]]]


class GetImageEmbeddingsRequest(BaseModel):
    image_paths: List[str]


class GetImageEmbeddingsResponse(BaseResponse):
    embeddings: Optional[List[List[float]]]


class GetImageCaptionRequest(BaseModel):
    image_path: List[str]


class GetImageCaptionResponse(BaseResponse):
    caption: Optional[List[str]]


class GetCaptionWithEmbeddingsRequest(BaseModel):
    image_paths: List[str]


class GetCaptionWithEmbeddingsResponse(BaseResponse):
    caption: Optional[List[str]]
    text_embeddings: Optional[List[List[float]]]
    image_embeddings: Optional[List[List[float]]]


class CreateIndexingTaskRequest(BaseModel):
    folder_path: str


class GetIndexingTaskRequest(BaseModel):
    task_id: str


class TaskData(BaseResponse):
    status: str
    caption_embeddings: Optional[List[List[float]]]
    image_embeddings: Optional[List[List[float]]]
    file_paths: Optional[List[str]]
    folder_path: str


class GetIndexingTaskResponse(BaseResponse):
    task_id: str
    status: str
    data: Optional[TaskData]


class IndexDirRequest(BaseModel):
    dir_path: str


class CreateIndexingTaskResponse(BaseResponse):
    task_id: Optional[str]


class IndexDirResponse(BaseResponse):
    index_id: Optional[str]


class GetAllIndexResponse(BaseResponse):
    data: Optional[List[Index]]


class GetIndexStatusResponse(BaseResponse):
    data: Optional[int]
    status_name: Optional[str]


class SearchByTextRequest(BaseSearchRequest):
    search_string: str


class BaseSearchResultResponse(BaseResponse):
    data: Optional[List[str]]


class SearchByImageRequest(BaseSearchRequest):
    pass


class DeleteIndexRequest(BaseModel):
    index_name: str


class DeleteIndexResponse(BaseResponse):
    data: Optional[str]
