from pydantic import BaseModel, Field

from schemas.artist import ArtistShort
from schemas.release_type import ReleaseTypeDetail
from schemas.track import TrackDetail, Disc


class AlbumShort(BaseModel):
    """
    Схема кратной информации альбома
    """

    id: int = Field(alias='album_id')
    title: str
    year: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "album_id": 26,
                "title": "Physical Graffiti",
                "price": "1975",
            }
        }
    }


class Albums(BaseModel):
    """
    Схема списка альбомов
    """

    artist: ArtistShort
    release_type: ReleaseTypeDetail
    items: list[AlbumShort] = []


class AlbumDetail(BaseModel):
    """
    Схема детальной информации об альбоме
    """

    id: int = Field(alias='album_id')
    title: str
    url: str
    year: str
    label: str
    cover_url: str
    music_rating: str
    avg_rating: str
    duration: str
    genre: str
    styles: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "album_id": 26,
                "title": "Physical Graffiti",
                "url": "https://www.allmusic.com/album/physical-graffiti-mw0000190771",
                "year": "1975",
                "label": "Atlantic",
                "cover_url": "https://rovimusic.rovicorp.com/image.jpg?c=TowcrF3hlzWFHHG_jQ6j2z6KsMttLlyBmmVTZ6_CLs0="
                             "&f=2",
                "music_rating": "9",
                "avg_rating": "10-6455",
                "duration": "01:22:51",
                "genre": "Pop/Rock, Blues",
                "styles": "Hard Rock, Album Rock, British Metal, Arena Rock, British Blues, Heavy Metal"
            }
        }
    }


class AlbumDisplay(BaseModel):
    """
    Схема отображения альбома
    """

    album: AlbumDetail
    artist: ArtistShort
    tracks: list[TrackDetail] | list[Disc]
