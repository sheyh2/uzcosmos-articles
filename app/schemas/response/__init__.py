from typing import List, Generic, TypeVar, Optional, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T', bound=BaseModel)


class Meta(BaseModel):
    per_page: Optional[int] = None
    total: Optional[int] = None
    current_page: Optional[int] = None
    last_page: Optional[int] = None


class BaseResponse(GenericModel, Generic[T]):
    code: int
    message: str
    data: Union[T, List[T], None] = None


class PaginationResponse(BaseResponse):
    meta: Optional[Meta] = None
