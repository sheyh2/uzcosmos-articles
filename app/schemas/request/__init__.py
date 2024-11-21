from pydantic import BaseModel, conint


class MetaParams(BaseModel):
    item_per_page: conint(ge=1, le=100) = 10
    page: conint(ge=1) = 1
