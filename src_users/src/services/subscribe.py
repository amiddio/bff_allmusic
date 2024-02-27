from datetime import datetime, timedelta

from databases.crud import Crud
from models.subscriber import SubscribeFormData, Subscriber, Subscriptions
from models.user import UserOut


class SubscribeService:

    @staticmethod
    async def save_subscription(user: UserOut, data: SubscribeFormData):
        subscriptions = []

        for artist_id in data.artist_ids:
            active_till = datetime.utcnow() + timedelta(days=data.days)

            subscription = await Crud.find_one(
                model=Subscriber, criteria={Subscriber.user.id: user.id, Subscriber.artist_id: artist_id}
            )

            if not subscription:
                subscription = Subscriber(user=user, artist_id=artist_id, active_till=active_till)
                await Crud.create(model=subscription)
            else:
                subscription.active_till = active_till
                await subscription.save()
            subscriptions.append(subscription)

        return Subscriptions(subscriptions=subscriptions)
