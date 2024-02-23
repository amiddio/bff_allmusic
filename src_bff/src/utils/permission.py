from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.requests import Request

from services.allmusic_service import AllmusicService
from services.user_service import UserService


class Permission:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login', scheme_name='JWT')

    async def __call__(
        self, request: Request, artist_id: int = None, album_id: int = None, token: str = Depends(oauth2_scheme)
    ):
        if not artist_id:
            if album_id:
                artist_id = await AllmusicService().get_artist_id(album_id=album_id)

        if not artist_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An artist cannot be detected"
            )

        await UserService().is_permission(artist_id=artist_id, headers=request.headers)


