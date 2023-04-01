from django.urls import path
from .views import RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', MyTokenObtainPairView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),
]
