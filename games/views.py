import logging

from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Platform

from .serializers import GameSerializer

logger = logging.getLogger(__name__)

def games_plain_django(request):
    data = list(Game.objects.values('id', 'title', 'genre', 'rating', 'released'))
    return JsonResponse(data, safe=False)


class HelloAPIView(APIView):
    def get(self, request):
        return Response({
            'message': 'Hello, DRF!',
            'status': 'It works on my machine',
        })


class GameListAPIView(APIView):
    def get(self, request):
        games = Game.objects.select_related("developer").prefetch_related(
            Prefetch("platforms",
                     queryset=Platform.objects.order_by("name"))
        )
        cached_data = cache.get("games:list:v1")
        if cached_data is not None:
            logger.info("Список игр отдан из кэша")
            return Response(cached_data)

        data = GameSerializer(games, many=True).data
        cache.set("games:list:v1", data, timeout=60)
        logger.info("Список игр сформирован из базы и сохранён в кэш")
        return Response(data)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            cache.delete("games:list:v1")
            logger.info("Создана игра id=%s", game.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Ошибка валидации при создании игры: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameDetailAPIView(APIView):
    def get_object(self, pk):
        queryset = Game.objects.select_related("developer").prefetch_related("platforms")
        return get_object_or_404(queryset, pk=pk)

    def get(self, request, pk):
        return Response(GameSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        return self.update(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def update(self, request, pk, partial):
        game = self.get_object(pk)
        serializer = GameSerializer(game, data=request.data, partial=partial)
        if serializer.is_valid():
            game = serializer.save()
            cache.delete("games:list:v1")
            logger.info("Обновлена игра id=%s", game.pk)
            return Response(serializer.data)
        logger.warning("Ошибка валидации при обновлении игры id=%s: %s", pk)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        game = self.get_object(pk)
        game.delete()
        cache.delete("games:list:v1")
        logger.info("Удалена игра id=%s", game.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
