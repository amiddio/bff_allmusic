# BFF Pattern Services

## Описание

Стэк: Docker, Python3.10, FastAPI, BeautifulSoup4, PostgreSQL, MongoDB, SQLAlchemy, Beanie, JWT, aiohttp, Pytest

Пример реализации микро сервисной архитектуры веб-приложения, используя паттерн проектирования Backend-for-Frontend (BFF).
Проект содержит три сервиса:

### 1. Allmusic сервис

Стэк: Python3.10, FastAPI, BeautifulSoup4, SQLAlchemy, PostgreSQL, Pytest

Содержит два основных функционала:

Первый - это парсер. Парсер, используя библиотеку BeautifulSoup, парсит сайт allmusic.com, находит на нем запрошенных исполнителей, альбомы, треки, и сохраняет в локальной БД.

Второй - json ответы. Используя эндпойнты можно просмотреть исполнителей, типы релизов с дискографией, и у каждого альбома, посмотреть список треков.

### 2. Users сервис

Стэк: Python3.10, FastAPI, Beanie, MongoDB, JWT, Pytest

Сервис хранит информацию о пользователях. Можно добавить нового пользователя, просмотреть его. Реализована возможность авторизации пользователя по токену. 
Также сервис содержит функционал для подписки пользователя на исполнителей из Allmusic сервиса.

### 3. BFF сервис

Стэк: Python3.10, FastAPI, aiohttp

Сервис выполняет роль контролера. Он принимает запросы от клиента. Делает соответствующие запросы к двум предыдущим сервисам, и формирует ответы, которые отправляет клиенту.

## Управление и настройка

### Сборка

* Создайте директорию (например: `d:/bff_allmusic`)
* Откройте консольную программу (например: `PowerShell`) и перейдите в созданную директорию `cd d:/bff_allmusic`
* Клонируйте проект с репозитория: `git clone https://github.com/amiddio/bff_allmusic.git .`
* В `d:/bff_allmusic/src_allmusic/src` создайте файл `.env` на основе `.env.example`
* В `d:/bff_allmusic/src_bff/src` создайте файл `.env` на основе `.env.example`
* В `d:/bff_allmusic/src_users/src` создайте файл `.env` на основе `.env.example`
* Запустите Docker
* Выполните команду: `docker-compose build`

### Запуск

* Перейдите в корень проекта `d:/bff_allmusic`
* Выполните команду: `docker-compose up`

### Остановка

* Перейдите в корень проекта `d:/bff_allmusic`
* Выполните команду: `docker-compose down`

### Pytests

* Перейдите в корень проекта `d:/bff_allmusic`
* Для запусков тестов сервиса Allmusic выполните команду `docker-compose exec web-app-allmusic pytest`
* Для запусков тестов сервиса Users выполните команду `docker-compose exec web-app-users pytest`

## Эндпойнты

### 1. Парсим allmusic.com

Url: `POST` `http://localhost:8080/api/v1/allmusic/parser`

Data: `{
    "seq": [
        "Haken", "Art Of Anarchy", "Gentle Giant"
    ]
}`

![Screenshot_1](/screenshots/Screenshot_1.png)

### 2. Список исполнителей

Url: `GET` `http://localhost:8080/api/v1/allmusic/artists`

![Screenshot_2](/screenshots/Screenshot_2.png)

### 3. Регистрацию нового пользователя

Url: `POST` `http://localhost:8080/api/v1/user/register`

Data: `{
    "email": "john.dow@home.com",
    "name": "John Dow",
    "password": "qwerty",
    "password_repeat": "qwerty"
}`

![Screenshot_3](/screenshots/Screenshot_3.png)

### 4. Авторизация пользователя

Url: `POST` `http://localhost:8080/api/v1/user/login`

Data: `{
    "username": "john.dow@home.com",
    "password": "qwerty"
}`

![Screenshot_4](/screenshots/Screenshot_4.png)

### 5. Информация о пользователе (необходима авторизация)

Url: `GET` `http://localhost:8080/api/v1/user/me`

![Screenshot_5](/screenshots/Screenshot_5.png)

### 6. Доступ к исполнителю без подписки (необходима авторизация)

Url: `GET` `http://localhost:8080/api/v1/allmusic/artist/3`

![Screenshot_6](/screenshots/Screenshot_6.png)

### 7. Подписка пользователя на исполнителей (необходима авторизация)

Url: `POST` `http://localhost:8080/api/v1/user/subscribe`

Data: `{
    "artist_ids": [3, 1, 2],
    "days": 30
}`

![Screenshot_7](/screenshots/Screenshot_7.png)

### 8. Доступ к исполнителю после подписки (необходима авторизация)

Url: `GET` `http://localhost:8080/api/v1/allmusic/artist/3`

![Screenshot_8](/screenshots/Screenshot_8.png)

### 9. Доступ к дискографии исполнителя (необходима авторизация)

Url: `GET` `http://localhost:8080/api/v1/allmusic/discography/3/1`

![Screenshot_9](/screenshots/Screenshot_9.png)

### 10. Доступ к альбому (необходима авторизация)

Url: `GET` `http://localhost:8080/api/v1/allmusic/album/17`

![Screenshot_10](/screenshots/Screenshot_10.png)
