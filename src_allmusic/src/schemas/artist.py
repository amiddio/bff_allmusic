from pydantic import BaseModel, Field

from schemas.release_type import ReleaseTypeDetail


class ArtistsRequest(BaseModel):
    """
    Схема запроса на парсинг исполнителей
    """

    seq: list[str]


class ArtistShort(BaseModel):
    """
    Схема краткой информации об исполнителе
    """

    id: int = Field(alias='artist_id')
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "artist_id": 7,
                "name": "Gentle Giant",
            }
        }
    }


class ArtistDetail(BaseModel):
    """
    Схема подробной информации об исполнителе
    """

    id: int = Field(alias='artist_id')
    name: str
    url: str
    genres: str
    decades: str
    release_types: list[ReleaseTypeDetail] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "artist_id": 7,
                "name": "Gentle Giant",
                "url": "https://www.allmusic.com/artist/gentle-giant-mn0000165162",
                "genres": "Pop/Rock",
                "decades": "1970s - 1980s",
            }
        }
    }
