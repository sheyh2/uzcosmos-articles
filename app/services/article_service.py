import hashlib
import os
import time
from typing import List, Tuple, BinaryIO, Optional

from fastapi import Depends, HTTPException, UploadFile, status
from app.core.config import settings
from app.models.article import Article, ArticleFile
from app.repositories.article_repository import ArticleRepository, ArticleFileRepository
from app.schemas.request.article import SearchParams


class ArticleService:
    def __init__(
            self,
            article_repository: ArticleRepository = Depends(ArticleRepository)
    ) -> None:
        self.article_repository = article_repository
        pass

    def search(self, search_params: SearchParams) -> Tuple[List[Article], int]:
        return self.article_repository.search(search_params)

    def get_by_id(self, id) -> Article:
        article = self.article_repository.get_by_id(id=id)
        if article is None:
            raise HTTPException(status_code=404, detail='Статья не найден!')

        return article

    def create(self, item: dict) -> Article:
        return self.article_repository.create(item)

    def update(self, article: Article, item: dict) -> Article:
        return self.article_repository.update(article, item)

    def delete(self, article: Article) -> bool:
        return self.article_repository.delete(article)


class ArticleFileService:
    def __init__(
            self,
            article_file_repository: ArticleFileRepository = Depends(ArticleFileRepository)
    ):
        self.article_file_repository = article_file_repository
        self.path = settings.UPLOAD_DIR
        pass

    def calculate_md5(self, image: BinaryIO) -> str:
        md5 = hashlib.md5()
        while chunk := image.read(8192):
            md5.update(chunk)
        image.seek(0)
        return md5.hexdigest()

    def create(self, image: UploadFile, article_id: int) -> ArticleFile | None:
        path = settings.UPLOAD_DIR
        extension = image.filename.split('.')[-1] if '.' in image.filename else 'unknown'
        md5 = self.calculate_md5(image.file)

        filename = f'article-{int(time.time())}'
        full_path = os.path.join(path, f'{filename}.{extension}')

        try:
            with open(full_path, 'wb') as f:
                f.write(image.file.read())
        except IOError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Ошибка записи файла: {e}'
            )

        return self.article_file_repository.create({
            'article_id': article_id,
            'name': filename,
            'path': path,
            'extension': extension,
            'md5': md5
        })

    def delete(self, article_file: Optional[ArticleFile]) -> bool:
        if article_file is None:
            return True

        if os.path.exists(article_file.image_full_path):
            os.remove(article_file.image_full_path)

        self.article_file_repository.delete(article_file)
