from pydantic import BaseModel


class ArticleResponse(BaseModel):
    id: int
    name: str
    description: str
    image_url: str = None
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class DeleteArticleResponse(BaseModel):
    id: int


class ArticleImageUploadResponse(BaseModel):
    image_url: str
