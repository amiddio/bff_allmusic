from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.album import AlbumDisplay, Albums
from schemas.artist import ArtistDetail
from schemas.pagination import PageParams, PagedResponseSchema
from services.album_service import AlbumService
from services.artist_service import ArtistService

router = APIRouter(prefix='/view')


@router.get('/artists', response_description="Get all artists", response_model=PagedResponseSchema)
async def get_all_artists(page_params: PageParams = Depends(), db: Session = Depends(get_db)) -> PagedResponseSchema:
    return await ArtistService(db=db).get_all(page_params=page_params)


@router.get('/artist/{artist_id}', response_description="Get artist detail by id", response_model=ArtistDetail)
async def get_artist_detail(artist_id: int, db: Session = Depends(get_db)) -> ArtistDetail:
    return await ArtistService(db=db).get_artist_by_id(artist_id=artist_id)


@router.post('/is_artists', response_description="Check if artist(s) exist")
async def is_artists(artist_ids: dict, db: Session = Depends(get_db)) -> list[int]:
    return await ArtistService(db=db).is_artists(artist_ids=artist_ids.get('artist_ids'))


@router.get('/discography/{artist_id}/{release_type_id}', response_description="Get albums", response_model=Albums)
async def get_albums(artist_id: int, release_type_id: int, db: Session = Depends(get_db)) -> Albums:
    return await AlbumService(db=db).get_albums(artist_id=artist_id, release_type_id=release_type_id)


@router.get('/album/{album_id}', response_description="Get album detail", response_model=AlbumDisplay)
async def get_album_detail(album_id: int, db: Session = Depends(get_db)) -> AlbumDisplay:
    return await AlbumService(db=db).get_album(album_id=album_id)


@router.get('/artist_id/{album_id}', response_description="Get artist_id by album_id")
async def get_artist_id(album_id: int, db: Session = Depends(get_db)) -> int:
    return await AlbumService(db=db).get_artist_id(album_id=album_id)
