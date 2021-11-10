from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Games, Player, GameReviews, GameRating
from django.contrib.auth.models import User



class RatingView(ViewSet):
    def create(self, request):
        player = Player.objects.get(user = request.auth.user)
        game = Games.objects.get(pk = request.data["game_id"])
        try:
            rating = GameRating.objects.create(
                game = game,
                player = player,
                rating = request.data["rating"]
            )
            return Response({'reason': 'Review Posted'}, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        player = Player.objects.get(user = request.auth.user)
        game = Games.objects.get(pk = request.data["game_id"])
        rating = GameRating.objects.get(pk=pk)
        rating.game = game
        rating.player = player
        rating.rating = request.data['rating']
        rating.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)