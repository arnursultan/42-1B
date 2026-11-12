import hashlib
import logging
from decimal import Decimal, InvalidOperation

from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .

def games_plain_django(request):
    data = list(Game.objects.values('id', 'title', 'genre', 'rating', 'released'))
    return JsonResponse(data, safe=False)


class HelloAPIView(APIView):
    def get(self, request):
        return Response({
            'message': 'Hello, DRF!',
            'status': 'It works on my machine',
        })

def game_to_dict(game):
    return{
        'id': game.id,
        'title': game.title,
        'genre': game.genre,
        'rating': game.rating,
        'released': game.released,
    }

class GameListAPIView(APIView):
    def get(self, request):
        games = Game.objects.all()
        return Response([game_to_dict(g) for g in games])

    def post(self, request):
        title = request.data['title']
        if not title:
            return Response(
                {'error': 'Алё, где название игры? Без названия это просто тайна.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        game = Game.objects.create(
            title=title,
            genre=request.data.get('genre', 'unknown'),
            rating=request.data.get('rating', 0),
            released=request.data.get('released'),
        )
        return Response(game_to_dict(game), status=status.HTTP_201_CREATED)

class GameDetailAPIView(APIView):
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        return Response(game_to_dict(game))

    def delete(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)