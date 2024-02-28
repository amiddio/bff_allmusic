import pytest

from starlette import status

from .fixtures.allmusic import *
from schemas.settings import Settings

settings = Settings()


def test_get_all_artists(artists, client):
    response = client.get(f"{settings.API_URI_PREFIX}/view/artists")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'total': 3, 'page': 1, 'size': 3,
        'items': [
            {'artist_id': 1, 'name': 'Artist1'},
            {'artist_id': 2, 'name': 'Artist2'},
            {'artist_id': 3, 'name': 'Artist3'}
        ]
    }


def test_get_artist_detail(artists, releases, albums, client):
    response = client.get(f"{settings.API_URI_PREFIX}/view/artist/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get('name') == 'Artist1'
    assert len(data.get('release_types')) == 3


def test_get_artist_discography(artists, releases, albums, client):
    response = client.get(f"{settings.API_URI_PREFIX}/view/discography/1/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get('artist').get('name') == 'Artist1'
    assert data.get('release_type').get('name') == 'Main'
    assert len(data.get('items')) == 2


def test_get_album_detail(albums, tracks, client):
    response = client.get(f"{settings.API_URI_PREFIX}/view/album/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get('album').get('title') == 'album 1'
    assert data.get('artist').get('name') == 'Artist1'
    assert len(data.get('tracks')) == 4


def test_get_artist_id_by_album_id(artists, albums, client):
    response = client.get(f"{settings.API_URI_PREFIX}/view/artist_id/4")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == '1'


def test_check_if_artists_exist(client):
    response = client.post(
        url=f"{settings.API_URI_PREFIX}/view/is_artists",
        json={'artist_ids': [1, 2, 3]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert data[0] == 1


def test_check_if_artists_exist_negative1(client):
    response = client.post(
        url=f"{settings.API_URI_PREFIX}/view/is_artists",
        json={'artist_ids': [1, 2222]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0] == 1


def test_check_if_artists_exist_negative2(client):
    response = client.post(
        url=f"{settings.API_URI_PREFIX}/view/is_artists",
        json={'artist_ids': [11111, 22222]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0


def test_parser(artists, releases, albums, client):
    parse_artist = 'Art of Anarchy'
    response = client.post(
        url=f"{settings.API_URI_PREFIX}/parser",
        json={'seq': [parse_artist]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()['response'][0]
    assert data.get(parse_artist).get('meta')[0] == f"Artist '{'Art of Anarchy'}' created or modified"
    assert len(data.get(parse_artist).get('albums')) > 0
