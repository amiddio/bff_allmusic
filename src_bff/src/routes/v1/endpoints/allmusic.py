from fastapi import APIRouter, Request, Security

from services.allmusic_service import AllmusicService
from utils.permission import Permission

router = APIRouter(prefix='/allmusic')


@router.get('/artists', response_description="Get all allmusic artists")
async def get_all_artists(request: Request) -> dict:
    return await AllmusicService().get_all_artists(request.query_params)


@router.get('/artist/{artist_id}', response_description="Get artist detail by id")
async def get_artist_detail(artist_id: int, _=Security(Permission())) -> dict:
    return await AllmusicService().get_artist_by_id(artist_id=artist_id)


@router.get('/discography/{artist_id}/{release_type_id}', response_description="Get albums")
async def get_artist_albums(artist_id: int, release_type_id: int, _=Security(Permission())) -> dict:
    return await AllmusicService().get_artist_albums(artist_id=artist_id, release_type_id=release_type_id)


@router.get('/album/{album_id}', response_description="Get album detail")
async def get_album_detail(album_id: int, _=Security(Permission())) -> dict:
    return await AllmusicService().get_album_by_id(album_id=album_id)


@router.post('/parser', response_description="Allmusic artists/albums/tracks parser")
async def do_parsing(artists: dict) -> None:
    return await AllmusicService().do_parsing(artists=artists)
