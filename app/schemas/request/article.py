from typing import Optional

from pydantic import BaseModel
from . import MetaParams


class ArticleResponse(BaseModel):
    id: int
    name: str
    description: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class DeleteArticleResponse(BaseModel):
    id: int


class CreateArticleRequest(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float


class UpdateArticleRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SearchParams(MetaParams):
    latitude: float
    longitude: float
    radius_km: int = 100


class ArticleFileRequest(BaseModel):
    article_id: int
    name: str
    path: str
    extension: str
    md5: str
