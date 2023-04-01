"""
ASGI config for myxiangqi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from room.middlewares import TokenAuthMiddleware
import chat.routing
import room.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myxiangqi.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            room.routing.websocket_urlpatterns,
        )
    ),
})