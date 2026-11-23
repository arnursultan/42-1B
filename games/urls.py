from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("games", views.GameViewSet, basename="game")
router.register(
    r"developers/(?P<developer_pk>\d+)/games",
    views.DeveloperGameViewSet,
    basename="developer-games",
)

urlpatterns = [
    path('plain/',  views.games_plain_django),
    path('hello/',  views.HelloAPIView.as_view()),
    path('',        include(router.urls)),
]