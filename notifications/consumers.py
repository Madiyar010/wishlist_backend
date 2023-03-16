from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.core.paginator import Paginator
from django.core.serializers import serialize
from channels.db import database_sync_to_async
from django.contrib.contenttypes.models import ContentType
import json
from friendship.models import FriendRequest, FriendList
from .utils import NotificationEncoder
from .models import Notification
from .constants import *


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Connect')
        await self.accept()

    async def disconnect(self, code):
        print('Disconnect')

    async def receive_json(self, content, **kwargs):
        command = content.get('command', None)
        print('Command', command)
        try:
            if command == 'get_notifications':
                payload = await get_notification(self.scope['user'], content['page_number'])
                if not payload:
                    raise Exception('Something went wrong')
                else:
                    payload = json.loads(payload)
                    await self.notifications_payload(payload['notifications'],
                                                     payload['new_page_number'])
        except Exception as e:
            raise e

    async def display_progress_bar(self, should_display):
        print('display progress bar', str(should_display))
        await self.send_json(
            {
                'progress_bar': should_display,
            },
        )

    async def notifications_payload(self, notifications, new_page_number):
        await self.send_json({
            'msg_type': MSG_TYPE_NOTIFICATIONS_PAYLOAD,
            'notifications': notifications,
            'new_page_number': new_page_number,
        })


@database_sync_to_async
def get_notification(user, page_number):
    if user.is_authenticated:
        friend_request_ct = ContentType.objects.get_for_model(FriendRequest)
        friend_list_ct = ContentType.objects.get_for_model(FriendList)
        notifications = Notification.objects.filter(target=user,
                                                    content_type__in=[friend_request_ct,
                                                                      friend_list_ct]).order_by('-timestamp')
        p = Paginator(notifications, DEFAULT_NOTIFICATION_PAGE_SIZE)
        payload = {}
        if len(notifications) > 0:
            if len(page_number) <= p.num_pages:
                s = NotificationEncoder()
                serialized_notifications = s.serialize(p.page(page_number).object_list)
                payload['notifications'] = serialized_notifications
                new_page_number = int(page_number) + 1
                payload['new_page_number'] = new_page_number
        else:
            return None
    else:
        raise Exception('User must be authenticated')
    return json.dumps(payload)
