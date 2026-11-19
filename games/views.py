import logging

from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .models import Game, Platform
from .serializers import GameSerializer

logger = logging.getLogger(__name__)


def games_plain_django(request):
    data = list(Game.objects.values("id", "title", "genre", "rating", "released"))
    return JsonResponse(data, safe=False)


class HelloAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello, DRF!", "status": "It works on my machine"})


class GameListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.select_related("developer").prefetch_related(
            Prefetch("platforms", queryset=Platform.objects.order_by("name"))
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            cache.delete("games:list:v1")
            logger.info("Создана игра")
        return response


class GameDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.select_related("developer").prefetch_related("platforms")

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self._update_and_invalidate(request, partial=False, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self._update_and_invalidate(request, partial=True, *args, **kwargs)

    def _update_and_invalidate(self, request, partial, *args, **kwargs):
        response = self.update(request, partial=partial, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            cache.delete("games:list:v1")
        return response

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        cache.delete("games:list:v1")
        return response


class DeveloperGameListAPIView(mixins.ListModelMixin, GenericAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(developer_id=self.kwargs["developer_pk"])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)