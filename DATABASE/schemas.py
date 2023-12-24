from pydantic import BaseModel


class IndexBase(BaseModel):
    index_id: str
    index_path: str
    index_status: int


class IndexCreate(IndexBase):
    pass


class Index(IndexBase):
    id: int

    class Config:
        from_attributes = True
