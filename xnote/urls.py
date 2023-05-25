from django.urls import path
from .views import CreateNoteView, GetNoteView, RandomXiangqiGameView, XiangqiGameView, OpeningXiangqiGameView, OpeningBookPlayedByMastersView

urlpatterns = [
    path('get', GetNoteView.as_view()),
    path('create', CreateNoteView.as_view()),
    path('random', RandomXiangqiGameView.as_view()),
    path('opening', OpeningXiangqiGameView.as_view()),
    path('game', XiangqiGameView.as_view()),
    path('opening-book', OpeningBookPlayedByMastersView.as_view()),
]
