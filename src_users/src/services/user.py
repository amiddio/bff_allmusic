from databases.crud import Crud
from models.user import UserOut, UserRegister, UserInDB, User
from utils.auth_jwt import AuthJWT


class UserService:

    @staticmethod
    async def get_user_by_email(email: str, incl_pass=False) -> User:
        if not incl_pass:
            return await Crud.find_one(model=UserOut, criteria={'email': email})
        else:
            return await Crud.find_one(model=UserInDB, criteria={'email': email})

    @staticmethod
    async def register_user(data: UserRegister) -> UserOut:
        user = UserInDB(
            email=data.email,
            name=data.name,
            hashed_password=AuthJWT().get_hashed_password(data.password)
        )
        await Crud.create(model=user)
        return UserOut(**user.dict())
