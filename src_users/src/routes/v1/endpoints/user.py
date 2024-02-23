from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from models.token import Token
from models.user import UserRegister, UserOut
from services.user import UserService
from utils.auth_jwt import AuthJWT
from utils.authenticate import Authenticate
from utils.permission import Permission

router = APIRouter(prefix='/users')


@router.post('/register',
             response_description="Create new user", response_model=UserOut,
             status_code=status.HTTP_201_CREATED)
async def create_user(form_data: UserRegister) -> UserOut:
    user = await UserService.get_user_by_email(email=form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    if not form_data.password or form_data.password != form_data.password_repeat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords must match"
        )

    return await UserService.register_user(data=form_data)


@router.post('/login', response_description="Login user", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await UserService.get_user_by_email(email=form_data.username, incl_pass=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth = AuthJWT()

    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(subject=user.email)
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/me", response_description="Get user data", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(user: UserOut = Security(Authenticate())) -> UserOut:
    return user


@router.get("/is_permission/{artist_id}", response_description="Is permission?", status_code=status.HTTP_200_OK)
async def is_permission(artist_id: int, permission: bool = Depends(Permission())) -> bool:
    return True
