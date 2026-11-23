import logging
import hashlib

from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Platform
from .serializers import GameSerializer

logger = logging.getLogger(__name__)
CACHE_TTL = 60


def cached_response(request, get_response):
    cache_key = "games-api:" + hashlib.md5(
        request.get_full_path().encode("utf-8")
    ).hexdigest()
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)

    response = get_response()
    if response.status_code == status.HTTP_200_OK:
        cache.set(cache_key, response.data, CACHE_TTL)
    return response


def invalidate_games_cache():
    cache.clear()


def games_plain_django(request):
    data = list(Game.objects.values("id", "title", "genre", "rating", "released"))
    return JsonResponse(data, safe=False)


class HelloAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello, DRF!", "status": "It works on my machine"})


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "genre", "developer__name"]
    ordering_fields = ["title", "rating", "released", "created_at"]
    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        queryset = Game.objects.select_related("developer").prefetch_related(
            Prefetch("platforms", queryset=Platform.objects.order_by("name"))
        )
        genre = self.request.query_params.get("genre")
        developer_id = self.request.query_params.get("developer")
        platform_id = self.request.query_params.get("platform")
        if genre:
            queryset = queryset.filter(genre=genre)
        if developer_id:
            queryset = queryset.filter(developer_id=developer_id)
        if platform_id:
            queryset = queryset.filter(platforms__id=platform_id)
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        return cached_response(request, lambda: super(GameViewSet, self).list(request, *args, **kwargs))

    def retrieve(self, request, *args, **kwargs):
        return cached_response(request, lambda: super(GameViewSet, self).retrieve(request, *args, **kwargs))

    def perform_create(self, serializer):
        serializer.save()
        logger.info("Создана игра")
        invalidate_games_cache()

    def perform_update(self, serializer):
        serializer.save()
        invalidate_games_cache()

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_games_cache()


class DeveloperGameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(developer_id=self.kwargs["developer_pk"]).select_related(
            "developer"
        ).prefetch_related(
            Prefetch("platforms", queryset=Platform.objects.order_by("name"))
        )

    def list(self, request, *args, **kwargs):
        return cached_response(request, lambda: super(DeveloperGameViewSet, self).list(request, *args, **kwargs))
