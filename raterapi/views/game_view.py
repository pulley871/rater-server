from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Games, Player, GameReviews
from django.contrib.auth.models import User

from raterapi.models.game_rating import GameRating


class GameView(ViewSet):
    def list(self, request):
        games = Games.objects.all()
        

        game_category = self.request.query_params.get('category', None)
        if game_category is not None:
            games = games.filter(category = game_category)
        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        player = Player.objects.get(user = request.auth.user)
        
        try:
            game = Games.objects.create(
                title = request.data['title'],
                description = request.data['description'],
                designer = request.data['designer'],
                year_released = request.data['year_released'],
                game_duration = request.data['game_duration'],
                number_of_players = request.data['number_of_players'],
                age_reccommendation = request.data['age_reccommendation'],
                host = player
            )
            game.category.set(request.data["category"])
            return Response({"Request": "Game Posted"}, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Gets Single Games"""
        player = Player.objects.get(user = request.auth.user)
        try:

            game = Games.objects.get(pk=pk)
            
            ratings = game.ratings.all()
            for rating in ratings:
                if player.id == rating.player_id:
                    game.rated = rating 
            
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def destroy(self,request, pk=None):
        try:
            game = Games.objects.get(pk=pk)
            game.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Games.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self,request, pk=None):
        player = Player.objects.get(user = request.auth.user)
        game = Games.objects.get(pk=pk)
        game.title = request.data['title']
        game.description = request.data['description']
        game.designer = request.data['designer']
        game.year_released = request.data['year_released']
        game.game_duration = request.data['game_duration']
        game.number_of_players = request.data['number_of_players']
        game.age_reccommendation = request.data['age_reccommendation']
        game.host = player
        game.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)






#Serializaers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
class HostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = ('user',)
class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = ('user',)
class ReviewSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = GameReviews
        fields = ('id', 'description','game', 'player' )
class RatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRating
        fields = ('id','rating',)       
class GameSerializer(serializers.ModelSerializer):
    host = HostSerializer()
    reviews = ReviewSerializer(many=True,required=None)
    rated = RatedSerializer(required=False)
    class Meta:
        model = Games
        fields = ('id', 'title', 'description','designer', 'year_released', 'game_duration', 'number_of_players', 'age_reccommendation', 'category', 'rating', 'host', 'reviews','rated',)
        depth = 1