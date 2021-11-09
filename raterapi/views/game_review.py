from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Games, Player, GameReviews
from django.contrib.auth.models import User


class ReviewView(ViewSet):
    def list(self, request):
        reviews = GameReviews.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={"request":request})
        return Response(serializer.data)

    def create(self, request):
        player = Player.objects.get(user=request.auth.user)
        game = Games.objects.get(pk=request.data['game_id'])
        try:
            GameReviews.objects.create(
                game = game,
                player = player,
                description = request.data['description']
            )
            return Response({'reason': 'Review Posted'}, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = ('user',)
class ReviewSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = GameReviews
        fields = ('id', 'game', 'player', 'description')
        depth = 1