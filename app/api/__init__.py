from typing import TypeVar, Optional, List, Union

from pydantic import BaseModel

from app.schemas.response import Meta, BaseResponse, PaginationResponse

T = TypeVar('T', bound=BaseModel)


def create_response(
        code: int = 200,
        message: str = 'Успешно',
        data: Union[T, List[T], None] = None,
        meta: Optional[Meta] = None
) -> BaseResponse:
    """
        Функция для формирования ответа.
        :param code: Код ответа
        :param message: Сообщение
        :param data: Данные (могут быть одной моделью, списком или None)
        :param meta: Метаинформация
        :return: Ответ в формате BaseResponse
    """

    if meta is None:
        return BaseResponse[T](
            code=code,
            message=message,
            data=data
        )

    return PaginationResponse[T](
        code=code,
        message=message,
        data=data,
        meta=meta
    )
