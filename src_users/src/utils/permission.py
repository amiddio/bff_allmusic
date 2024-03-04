from datetime import datetime
from fastapi import Security, HTTPException
from starlette import status

from databases.crud import Crud
from models.subscriber import Subscriber
from models.user import UserOut
from utils.authenticate import Authenticate


class Permission:
    """
    Класс проверяет есть ли у пользователя права для просмотра исполнителя
    """

    async def __call__(self, artist_id: int, user: UserOut = Security(Authenticate())) -> bool:

        subscription = await Crud.find_one(
            model=Subscriber, criteria={Subscriber.user.id: user.id, Subscriber.artist_id: artist_id}
        )

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User '{user.email}' has not permission to access to artist ID{artist_id}"
            )

        if subscription.active_till < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Subscription has expired for user '{user.email}' and artist ID{artist_id}"
            )

        return True
