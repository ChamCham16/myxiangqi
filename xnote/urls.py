from django.urls import path
from .views import CreateNoteView, GetNoteView

urlpatterns = [
    path('get', GetNoteView.as_view()),
    path('create', CreateNoteView.as_view()),
]
