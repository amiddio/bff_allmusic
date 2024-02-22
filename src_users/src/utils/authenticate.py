from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from services.user import UserService
from utils.auth_jwt import AuthJWT


class Authenticate:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        if not token:
            await self.__raise_exception(msg="Sign in for access", status_code=status.HTTP_403_FORBIDDEN)

        payload: dict = {}
        try:
            payload = AuthJWT().decode_token(token=token)

            if datetime.fromtimestamp(payload.get('exp', 0)) < datetime.now():
                await self.__raise_exception(msg="Token expired", status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            await self.__raise_exception(msg="Could not validate credentials", status_code=status.HTTP_403_FORBIDDEN)

        user = await UserService.get_user_by_email(email=payload.get('sub', None))
        if not user:
            await self.__raise_exception(msg="Could not find user", status_code=status.HTTP_404_NOT_FOUND)

        return user

    async def __raise_exception(self, msg: str, status_code: int) -> None:
        raise HTTPException(
            status_code=status_code,
            detail=msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
