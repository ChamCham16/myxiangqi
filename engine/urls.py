from django.urls import path
from .views import XQlightSearchView, PikafishSearchView

urlpatterns = [
    path('xqlight/search', XQlightSearchView.as_view()),
    path('pikafish/search', PikafishSearchView.as_view()),
]