from fastapi import APIRouter, Security
from starlette import status

from models.subscriber import SubscribeFormData, Subscriptions
from models.user import UserOut
from services.subscribe import SubscribeService
from utils.authenticate import Authenticate

router = APIRouter(prefix='/subscribe')


@router.post('', response_description="Subscribe user to artist(s)", status_code=status.HTTP_201_CREATED)
async def subscribe_user(form_data: SubscribeFormData, user: UserOut = Security(Authenticate())) -> Subscriptions:
    # host = str(request.client.host)
    # print(host)
    return await SubscribeService.save_subscription(user=user, data=form_data)
