from pydantic import BaseModel, conint
from schemas.artist import ArtistShort


class PageParams(BaseModel):
    """
    Request query params for paginated API
    """

    page: conint(ge=1) = 1
    size: conint(ge=1, le=1000) = 3

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 2,
                "size": 3,
            }
        }
    }


class PagedResponseSchema(BaseModel):
    """
    Response schema for any paged API
    """

    total: int
    page: int
    size: int
    items: list[ArtistShort]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 9,
                "page": 2,
                "size": 3,
            }
        }
    }
