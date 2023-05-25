from django.urls import path
from .views import CreateBookView, GetBookView, CreateXiangqiBookView, XiangqiBookView, CreateXiangqiSectionView, XiangqiSectionView, CreateXiangqiScriptView, XiangqiScriptView, UpdateXiangqiScriptView, ReadBookView

urlpatterns = [
    path('create', CreateBookView.as_view()),
    path('all', GetBookView.as_view()),
    path('create-book', CreateXiangqiBookView.as_view()),
    path('all-books', XiangqiBookView.as_view()),
    path('create-section', CreateXiangqiSectionView.as_view()),
    path('all-sections', XiangqiSectionView.as_view()),
    path('create-script', CreateXiangqiScriptView.as_view()),
    path('all-scripts', XiangqiScriptView.as_view()),
    path('update-script', UpdateXiangqiScriptView.as_view()),
    path('read', ReadBookView.as_view()),
]