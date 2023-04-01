from django.urls import path
from .views import CreateXiangqiRoomView, GetXiangqiRoomView

urlpatterns = [
    path('create', CreateXiangqiRoomView.as_view()),
    path('all', GetXiangqiRoomView.as_view()),
]
