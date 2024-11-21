from typing import List, Tuple
from sqlalchemy import func
from app.models.article import Article, ArticleFile
from app.repositories import Repository
from app.schemas.request.article import SearchParams


class ArticleRepository(Repository):
    def search(self, search_params: SearchParams) -> Tuple[List[Article], int]:
        EARTH_RADIUS_KM = 6371.0
        distance_formula = (
                EARTH_RADIUS_KM
                * func.acos(
                    func.cos(func.radians(search_params.latitude))
                    * func.cos(func.radians(Article.latitude))
                    * func.cos(func.radians(Article.longitude) - func.radians(search_params.longitude))
                    + func.sin(func.radians(search_params.latitude)) * func.sin(func.radians(Article.latitude))
                )
        )

        article_query = (self.db.query(Article)
                         .filter(distance_formula <= search_params.radius_km)
                         .order_by(distance_formula))
        total_items = article_query.count()

        articles = (article_query
                    .offset((search_params.page - 1) * search_params.item_per_page)
                    .limit(search_params.item_per_page)
                    .all())

        return articles, total_items

    def get_by_id(self, id: int) -> Article | None:
        return self.db.query(Article).filter(id == Article.id).first()

    def create(self, item: dict) -> Article | None:
        article = Article(**item)
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def update(self, article: Article, item: dict) -> Article:
        for key, val in item.items():
            setattr(article, key, val)
            pass
        self.db.commit()
        self.db.refresh(article)

        return article

    def delete(self, article: Article) -> bool:
        self.db.delete(article)
        self.db.commit()

        return True


class ArticleFileRepository(Repository):
    def create(self, item: dict) -> ArticleFile | None:
        article_file = ArticleFile(**item)
        self.db.add(article_file)
        self.db.commit()
        self.db.refresh(article_file)

        return article_file

    def delete(self, article_file: ArticleFile) -> bool:
        self.db.delete(article_file)
        self.db.commit()

        return True
