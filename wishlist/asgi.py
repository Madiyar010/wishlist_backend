import os
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from notifications.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishlist.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path(r'ws/notification/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
            ])
        )
    )
})
