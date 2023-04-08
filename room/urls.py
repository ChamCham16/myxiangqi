from django.urls import path
from .views import CreateRoomView, GetRoomView

urlpatterns = [
    path('create-room', CreateRoomView.as_view()),
    path('all-rooms', GetRoomView.as_view()),
]
