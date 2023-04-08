from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/room/<str:room_name>/', consumers.RoomConsumer.as_asgi()),
    path('ws/server/<str:server_name>/', consumers.ServerConsumer.as_asgi()),
]