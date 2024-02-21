from bs4 import Tag

from allmusic.allmusic_base import AllmusicBase
from models.track import Track
from services.album_service import AlbumService
from services.track_service import TrackService


class TrackGraber(AllmusicBase):
    """
    Класс парсинга треков
    """

    async def grab(self, album_id: int) -> None:
        """
        Метод запускающий парсинг

        :param album_id: int
        :return: None
        """

        # Получаем альбом по id
        album = AlbumService(db=self._db).get(album_id)

        # Контейнер со списком треков
        soup_track_container = await self.get_html(
            url=type(self).__get_track_listing_url(url=album.url),
            headers=dict({'Referer': album.url})
        )

        # Получаем треки в блоках дисков для дальнейшего парсинга
        all_disks = soup_track_container.find_all("div", class_="disc")
        for disc in all_disks:
            disc_num = disc.h3.text if disc.h3 else ''
            for track in disc.find_all("div", class_="track"):
                num = await self.__get_track_number(content=track)
                title = await self.__get_track_title(content=track)
                composers = await self.__get_track_composers(content=track)
                performers = await self.__get_track_performers(content=track)
                duration = await self.__get_track_duration(content=track)
                track = Track(
                    album_id=album_id, num=num, title=title, disc=disc_num, duration=duration,
                    composers=composers, performers=performers
                )
                # Сохраняем трек в БД
                TrackService(db=self._db).create(track=track)

    async def __get_track_number(self, content: Tag) -> str:
        """
        Находим номер трека в альбоме

        :param content: Tag
        :return: str
        """

        return content.find('div', class_='trackNum').text

    async def __get_track_title(self, content: Tag) -> str:
        """
        Название трека

        :param content: Tag
        :return: str
        """

        track_title = content.find('div', class_='meta').find('div', class_='title')
        if track_title.a:
            track_title = track_title.a.text
        else:
            track_title = track_title.text
        return track_title

    async def __get_track_composers(self, content: Tag) -> str:
        """
        Находим список композиторов

        :param content: Tag
        :return: str
        """

        track_composer = content.find('div', class_='meta').find('div', class_='composer')
        if track_composer:
            composers = []
            for c in track_composer.find_all('a'):
                composers.append(c.text)
            return ' / '.join(composers)
        else:
            return ''

    async def __get_track_performers(self, content: Tag) -> str:
        """
        Находим исполнителей

        :param content: Tag
        :return: str
        """

        track_performer = content.find('div', class_='performer')
        if track_performer:
            performers = []
            for p in track_performer.find_all('a'):
                performers.append(p.text)
            return ' / '.join(performers)
        else:
            return ''

    async def __get_track_duration(self, content: Tag) -> str:
        """
        Находим длительность трека

        :param content: Tag
        :return: str
        """

        return content.find('div', class_='duration').text.strip()

    @staticmethod
    def __get_track_listing_url(url: str) -> str:
        """
        Формируем url для парсинга треков

        :param url: str
        :return: str
        """

        return f"{url}/trackListingAjax"
