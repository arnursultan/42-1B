from django.urls import path
from . import views

urlpatterns = [
    path('plain/',           views.games_plain_django),
    path('hello/',            views.HelloAPIView.as_view()),
    path('games/',           views.GameListAPIView.as_view()),
    path('games/<int:pk>/',  views.GameDetailAPIView.as_view()),
]