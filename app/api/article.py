import math
from typing import List

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form

from app.schemas.response import Meta, BaseResponse, PaginationResponse
from app.schemas.request.article import (
    CreateArticleRequest,
    UpdateArticleRequest,
    SearchParams
)
from app.schemas.response.article import ArticleResponse, DeleteArticleResponse, ArticleImageUploadResponse
from app.services.article_service import ArticleService, ArticleFileService
from app.api import create_response

router = APIRouter(prefix='/articles', tags=['article'])


@router.post('/search', response_model=PaginationResponse[List[ArticleResponse]])
async def search(
        query_params: SearchParams = Query(...),
        article_service: ArticleService = Depends(ArticleService)
):
    articles, total_items = article_service.search(query_params)

    return create_response(
        data=[ArticleResponse.from_orm(article) for article in articles],
        meta=Meta(
            per_page=query_params.item_per_page,
            total=total_items,
            current_page=query_params.page,
            last_page=math.ceil(total_items / query_params.item_per_page),
        )
    )


@router.post('', response_model=BaseResponse[ArticleResponse])
async def create(
        create_article_request: CreateArticleRequest,
        article_service: ArticleService = Depends(ArticleService)
):
    return create_response(
        data=ArticleResponse.from_orm(article_service.create(create_article_request.dict()))
    )


@router.get('/{id}', response_model=BaseResponse[ArticleResponse])
async def show(
        id: int,
        article_service: ArticleService = Depends(ArticleService)
):
    return create_response(
        data=ArticleResponse.from_orm(article_service.get_by_id(id=id))
    )


@router.put('/{id}', response_model=BaseResponse[ArticleResponse])
async def update(
        id: int,
        update_article_request: UpdateArticleRequest,
        article_service: ArticleService = Depends(ArticleService)
):
    article = article_service.get_by_id(id=id)

    return create_response(
        data=ArticleResponse.from_orm(
            article_service.update(article, update_article_request.model_dump(exclude_unset=True)))
    )


@router.delete('/{id}', response_model=BaseResponse[DeleteArticleResponse])
async def delete(
        id: int,
        article_service: ArticleService = Depends(ArticleService),
        article_file_service: ArticleFileService = Depends(ArticleFileService)
):
    article = article_service.get_by_id(id)
    article_file_service.delete(article.article_file)
    article_service.delete(article)

    return create_response(
        data=DeleteArticleResponse(id=id)
    )


@router.post('/upload-image', response_model=BaseResponse[ArticleImageUploadResponse])
async def upload_image(
        image: UploadFile = File(...),
        article_id: int = Form(...),
        article_service: ArticleService = Depends(ArticleService),
        article_file_service: ArticleFileService = Depends(ArticleFileService)
):
    article = article_service.get_by_id(id=article_id)
    old_article_file = article.article_file

    article_file = article_file_service.create(image, article_id)
    article_file_service.delete(old_article_file)

    return create_response(
        data=ArticleImageUploadResponse(image_url=article_file.image_url)
    )
