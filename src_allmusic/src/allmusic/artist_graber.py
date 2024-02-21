from bs4 import Tag

from allmusic.album_graber import AlbumGraber
from allmusic.allmusic_base import AllmusicBase
from models.artist import Artist
from schemas.artist import ArtistsRequest
from services.artist_service import ArtistService


class ArtistGraber(AllmusicBase):
    """
    Класс парсинга музыкальных исполнителей и групп
    """

    __ARTIST_URL = 'https://www.allmusic.com/search/artists/{artist}'

    async def grab(self, artists: ArtistsRequest) -> list:
        """
        Метод запускающий парсинг

        :param artists: ArtistsRequest
        :return: list
        """

        result = []
        for artist in artists.seq:
            result.extend(
                await self.__find_artist(artist)
            )
        return result

    async def __find_artist(self, qw: str) -> list:
        """
        Метод парсит страницу с исполнителями, и сохраняет найденных исполнителей в БД

        :param qw: str
        :return: list
        """

        qw: str = qw.lower()
        url: str = self.__ARTIST_URL.format(artist=qw)
        result: list[dict] = []

        soup = await self.get_html(url=url)

        artists = await self.__get_artists_list(content=soup)
        for artist in artists:
            name, url = await self.__get_block_name(content=artist)
            if name and name.lower() == qw:

                # Создаем объект исполнителя
                art = Artist(
                    name=name, url=url,
                    genres=await self.__get_block_genres(content=artist),
                    decades=await self.__get_block_decades(content=artist)
                )
                # Сохраняем исполнителя
                artist_id = ArtistService(db=self._db).create_or_update(artist=art)

                # Запускаем парсинг всех альбомов исполнителя
                albums = await AlbumGraber(db=self._db).grab(artist_id=artist_id)

                result.append({
                    str(art): {
                        'meta': [f"Artist '{art}' created or modified"],
                        'albums': albums,
                    }
                })
        if not result:
            result.append({
                qw: {'meta': [f"Artist '{qw}' not found"]}
            })

        return result

    async def __get_artists_list(self, content: Tag) -> list[Tag]:
        """
        Находим всех артистов и возвращаем их списком

        :param content: Tag
        :return: list[Tag]
        """

        return content.find_all('div', {'class': 'artist'})

    async def __get_block_name(self, content: Tag) -> tuple | None:
        """
        Возвращаем исполнителя и url

        :param content: Tag
        :return: tuple | None
        """

        if block_name := content.find('div', class_='name').find('a'):
            artist_name = block_name.text
            artist_link = block_name['href']
            return artist_name, artist_link

    async def __get_block_genres(self, content: Tag) -> str | None:
        """
        Возвращаем жанры

        :param content: Tag
        :return: str | None
        """

        if res := content.find('div', class_='genres'):
            return res.text.strip()

    async def __get_block_decades(self, content: Tag) -> str | None:
        """
        Возвращаем декады творчества

        :param content: Tag
        :return: str | None
        """

        if res := content.find('div', class_='decades'):
            return res.text.strip()
