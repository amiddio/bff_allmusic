from abc import ABC, abstractmethod
from typing import Any

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status


class AllmusicBase(ABC):
    """
    Базовый класс парсеров сайта allmusic
    """

    __headers = ({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    })

    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def grab(self, *args, **kwargs) -> Any:
        pass

    def get_headers(self) -> dict[str, str]:
        """
        Метод возвращает словарь с загаловками запроса по умолчанию

        :return: dict
        """

        return self.__headers

    async def get_html(self, url: str, headers: dict = None) -> BeautifulSoup:
        """
        Метод делает запрос на некий url и возвращает объект BeautifulSoup, для дальнейшего разбора

        :param url: str
        :param headers: dict
        :return: BeautifulSoup
        """

        headers = self.get_headers() if not headers else self.get_headers() | headers

        async with ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status == status.HTTP_200_OK:
                    webpage = await response.text()
                    return BeautifulSoup(webpage, 'html.parser')

                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                    detail=f"Scraper didn't succeed in getting data:\n"
                                           f"\turl: {url}\n"
                                           f"\tstatus code: {response.status}\n")
