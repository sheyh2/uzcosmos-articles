from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from app.core.config import asset
from app.core.database import base


class Article(base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relations
    article_file: Mapped['ArticleFile'] = relationship(back_populates='article')

    @property
    def image_url(self):
        return self.article_file.image_url

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_updated_at(self) -> datetime:
        return self.updated_at


class ArticleFile(base):
    __tablename__ = 'article_files'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    name = Column(String(length=255))
    path = Column(String(length=255))
    extension = Column(String(length=25))
    md5 = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # Relations
    article: Mapped['Article'] = relationship(back_populates='article_file')

    def get_id(self) -> int:
        return self.id

    def get_article_id(self) -> int:
        return self.article_id

    def get_name(self) -> str:
        return self.name

    def get_path(self) -> str:
        return self.path

    def get_extension(self) -> str:
        return self.extension

    def get_md5(self) -> str:
        return self.md5

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_updated_at(self) -> datetime:
        return self.updated_at

    @property
    def image_url(self) -> str:
        image = '{path}/{filename}.{extension}'.format(
            path=self.get_path(),
            filename=self.get_name(),
            extension=self.get_extension()
        )

        return asset(image)

    @property
    def image_full_path(self) -> str:
        return '{path}/{filename}.{extension}'.format(
            path=self.get_path(),
            filename=self.get_name(),
            extension=self.get_extension()
        )
