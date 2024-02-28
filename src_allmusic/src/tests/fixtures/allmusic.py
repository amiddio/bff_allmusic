import pytest

from models import Artist, Album
from models.track import Track

from services.album_service import AlbumService
from services.artist_service import ArtistService
from services.release_type_service import ReleaseTypeService
from services.track_service import TrackService


@pytest.fixture
def artists(db):
    artist_service = ArtistService(db=db)
    artist1 = Artist(name='Artist1', url='artist1_url', genres='pop/rock', decades='1970-1980')
    artist2 = Artist(name='Artist2', url='artist2_url', genres='pop/rock', decades='1990-2000')
    artist3 = Artist(name='Artist3', url='artist3_url', genres='pop/rock', decades='2000-2010')
    artist_service.create_or_update(artist=artist1)
    artist_service.create_or_update(artist=artist2)
    artist_service.create_or_update(artist=artist3)


@pytest.fixture
def releases(db):
    rt_service = ReleaseTypeService(db=db)
    rt_service.get_release_type(release_type='main', name='Main')
    rt_service.get_release_type(release_type='compilations', name='Compilations')
    rt_service.get_release_type(release_type='singles', name='Singles & EPs')


@pytest.fixture
def albums(db):
    album_service = AlbumService(db=db)
    album1 = Album(
        title='album 1', url='album1_url', year='1995', label='Nuclear Blast', cover_url='cover_url',
        music_rating='9', avg_rating='9-238', duration='', genre='', styles='',
        artist_id=1, release_type_id=1
    )
    album2 = Album(
        title='album 2', url='album2_url', year='1997', label='One Way Records', cover_url='cover_url',
        music_rating='9', avg_rating='9-578', duration='', genre='', styles='',
        artist_id=1, release_type_id=2
    )
    album3 = Album(
        title='album 3', url='album3_url', year='2005', label='Vertigo', cover_url='cover_url',
        music_rating='8', avg_rating='8-745', duration='', genre='', styles='',
        artist_id=1, release_type_id=3
    )
    album4 = Album(
        title='album 4', url='album4_url', year='2012', label='Nuclear Blast', cover_url='cover_url',
        music_rating='8', avg_rating='8-756', duration='', genre='', styles='',
        artist_id=1, release_type_id=1
    )
    album_service.create_or_update(album=album1)
    album_service.create_or_update(album=album2)
    album_service.create_or_update(album=album3)
    album_service.create_or_update(album=album4)


@pytest.fixture
def tracks(db):
    track_service = TrackService(db=db)
    track1 = Track(
        album_id=1, num='1', title='track name 1', disc='', duration='5:06',
        composers='Michael Romeo', performers='Symphony X'
    )
    track2 = Track(
        album_id=1, num='2', title='track name 2', disc='', duration='3:25',
        composers='Michael Romeo', performers='Symphony X'
    )
    track3 = Track(
        album_id=1, num='3', title='track name 3', disc='', duration='12:44',
        composers='Michael Romeo', performers='Symphony X'
    )
    track4 = Track(
        album_id=1, num='4', title='track name 4', disc='', duration='9:10',
        composers='Michael Romeo', performers='Symphony X'
    )
    track_service.create(track=track1)
    track_service.create(track=track2)
    track_service.create(track=track3)
    track_service.create(track=track4)
