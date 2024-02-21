from bs4 import NavigableString, Tag

from allmusic.allmusic_base import AllmusicBase
from allmusic.track_graber import TrackGraber
from models import Album
from models.artist import Artist
from services.album_service import AlbumService
from services.artist_service import ArtistService
from services.release_type_service import ReleaseTypeService
from services.track_service import TrackService


class AlbumGraber(AllmusicBase):
    """
    Класс парсинга альбомов
    """

    async def grab(self, artist_id: int) -> list:
        """
        Метод запускающий парсинг

        :param artist_id: int
        :return: list
        """

        result: list[str] = []

        # Получаем объект исполнителя
        artist = ArtistService(db=self._db).get(artist_id)

        # Получаем список релизов (студийные альбомы, синглы и т.д.)
        soup = await self.get_html(
            url=type(self).__get_discography_url(artist.url), headers=dict({'Referer': artist.url})
        )
        release_types = soup.find('select', id='releaseType').find_all('option')

        for rel in release_types:
            if rel['value'] == 'all':
                continue

            rel_type_id = ReleaseTypeService(db=self._db).get_release_type(
                release_type=rel['value'], name=rel.text
            ).id

            # Парсим релиз и находим контент с альбомами
            soup_albums_table = await self.get_html(
                url=type(self).__get_discography_url(artist.url, rel['value']),
                headers=dict({'Referer': artist.url})
            )

            # Получаем таблицу с альбомами
            discography_table = soup_albums_table.find('table', class_='discographyTable').tbody.children
            for tr in discography_table:
                if isinstance(tr, NavigableString):
                    continue

                # Сохраняем альбом в БД
                album_id, album = await self.__save_album_info(tr=tr, artist=artist, rel_type_id=rel_type_id)
                result.append(str(album))

                # Если списка песен альбома еще не существует, парсим их
                if not TrackService(db=self._db).is_tracks(album_id=album_id):
                    await TrackGraber(db=self._db).grab(album_id=album_id)

        return result

    async def __save_album_info(self, tr: Tag, artist: Artist, rel_type_id: int) -> tuple[int, Album]:
        """
        Создаем объект альбома и сохраняем его в БД

        :param tr: Tag
        :param artist: Artist
        :param rel_type_id: int
        :return: tuple[int, Album]
        """

        album_service = AlbumService(db=self._db)

        # Сохраняем основную информацию об альбоме
        title = await self.__get_album_title(content=tr)
        url = await self.__get_album_url(content=tr)
        year = await self.__get_album_year(content=tr)
        label = await self.__get_album_label(content=tr)
        cover_url = await self.__get_album_cover_url(content=tr)
        music_rating = await self.__get_album_music_rating(content=tr)
        avg_rating = await self.__get_album_avg_rating(content=tr)
        album = Album(
            title=title, url=url, year=year, label=label, cover_url=cover_url, music_rating=music_rating,
            avg_rating=avg_rating, artist_id=artist.id, release_type_id=rel_type_id
        )

        album_id = album_service.create_or_update(album=album)

        # Сохраняем дополнительную информацию об альбоме
        await self.__addition_info(album_service=album_service, album_id=album_id, album_url=url)

        return album_id, album

    async def __addition_info(self, album_service: AlbumService, album_id: int, album_url: str) -> None:
        """
        Обновляем альбом дополнительной информацией

        :param album_service: AlbumService
        :param album_id: int
        :param album_url: str
        :return: None
        """

        soup = await self.get_html(url=album_url)
        duration = await self.__get_album_duration(content=soup)
        genre = await self.__get_album_genres(content=soup)
        styles = await self.__get_album_styles(content=soup)
        album_service.update(album_id, {
            Album.duration: duration, Album.genre: genre, Album.styles: styles
        })

    async def __get_album_duration(self, content: Tag) -> str:
        """
        Находим общую продолжительность альбома

        :param content: Tag
        :return: str
        """

        duration = content.find('div', class_='duration')
        if duration:
            return duration.span.text
        else:
            return ''

    async def __get_album_genres(self, content: Tag) -> str:
        """
        Находим жанры альбома

        :param content: Tag
        :return: str
        """

        genre = content.find('div', class_='genre')
        if genre:
            genres = []
            for g in genre.div.find_all('a'):
                genres.append(g.text)
            return ', '.join(genres)
        else:
            return ''

    async def __get_album_styles(self, content: Tag) -> str:
        """
        Находим стили альбома

        :param content: Tag
        :return: str
        """

        style = content.find('div', class_='styles')
        if style:
            styles = []
            for s in style.div.find_all('a'):
                styles.append(s.text)
            return ', '.join(styles)
        else:
            return ''

    async def __get_album_title(self, content: Tag) -> str:
        """
        Находим название альбома

        :param content: Tag
        :return: str
        """

        return content.find('td', class_='meta')['data-text']

    async def __get_album_url(self, content: Tag) -> str:
        """
        Находим url альбома

        :param content: Tag
        :return: str
        """

        return content.find('td', class_='meta').span.div.a['href']

    async def __get_album_year(self, content: Tag) -> str:
        """
        Находим год выхода альбома

        :param content: Tag
        :return: str
        """

        return content.find('td', class_='year').text.strip()

    async def __get_album_label(self, content: Tag) -> str:
        """
        Находим студию записи альбома

        :param content: Tag
        :return: str
        """

        label = content.find('td', class_='meta').find('span', class_='label')
        if label:
            return label.a.text
        return ''

    async def __get_album_cover_url(self, content: Tag) -> str:
        """
        Находим url на обложку альбома

        :param content: Tag
        :return: str
        """

        url = content.find('td', class_='cover').a.img['data-src']
        if 'no_image' in url:
            return ''
        return url.replace('&amp;', '&')

    async def __get_album_music_rating(self, content: Tag) -> str:
        """
        Находим рейтинг критиков альбома

        :param content: Tag
        :return: str
        """

        return content.find('td', class_='musicRating')['data-text']

    async def __get_album_avg_rating(self, content: Tag) -> str:
        """
        Находим рейтинг слушателей альбома

        :param content: Tag
        :return: str
        """

        return content.find('td', class_='avgRating')['data-text']

    @staticmethod
    def __get_discography_url(url: str, release_type: str = '') -> str:
        """
        Формируем url для парсинга альбомов

        :param url: str
        :param release_type: str
        :return: str
        """

        release_type = f'/{release_type}' if release_type else release_type
        return f"{url}/discographyAjax{release_type}"

