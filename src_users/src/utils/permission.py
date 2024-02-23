from fastapi import Security, HTTPException
from starlette import status

from models.user import UserOut
from utils.authenticate import Authenticate


class Permission:

    async def __call__(self, artist_id: int, user: UserOut = Security(Authenticate())):
        # print(artist_id, user)
        #
        # raise HTTPException(
        #     status_code=status.HTTP_403_FORBIDDEN,
        #     detail=f"User '{user.email}' has not permission to access to artist ID{artist_id}"
        # )

        return True
