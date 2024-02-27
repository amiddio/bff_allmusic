from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

from services.allmusic_service import AllmusicService
from services.user_service import UserService

router = APIRouter(prefix='/user')


@router.post('/register', response_description="New user register", status_code=status.HTTP_201_CREATED)
async def register_new_user(form_data: dict) -> dict:
    return await UserService().register_user(user_data=form_data)


@router.post('/login', response_description="User login", status_code=status.HTTP_200_OK)
async def login_user(form_data: dict) -> dict:
    return await UserService().login_user(login_data=form_data)


@router.get("/me", response_description="Get logged-in user data", status_code=status.HTTP_200_OK)
async def get_logged_in_user(request: Request) -> dict:
    return await UserService().get_user(headers=request.headers)


@router.post('/subscribe', response_description="Subscribe user to artist(s)", status_code=status.HTTP_201_CREATED)
async def subscribe_user(request: Request, data: dict) -> dict:
    if ids := await AllmusicService().is_artists_exist(artist_ids=data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Artist with id {ids} is not exist in DB of Allmusic service"
        )

    return await UserService().subscribe_user(data=data, headers=request.headers)
