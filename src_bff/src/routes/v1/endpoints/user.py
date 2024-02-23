from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from services.user_service import UserService

router = APIRouter(prefix='/user')


@router.post('/register', response_description="New user register")
async def register_new_user(form_data: dict) -> dict:
    return await UserService().register_user(user_data=form_data)


@router.post('/login', response_description="User login", status_code=status.HTTP_200_OK)
async def login_user(form_data: dict) -> dict:
    return await UserService().login_user(login_data=form_data)


@router.get("/me", response_description="Get logged-in user data", status_code=status.HTTP_200_OK)
async def get_logged_in_user(request: Request) -> dict:
    return await UserService().get_user(headers=request.headers)
