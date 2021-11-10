from django.db import models
from django.db.models.deletion import CASCADE

from raterapi.models import category
from .game_rating import GameRating
class Games(models.Model):
    title = models.TextField(max_length=30)
    description = models.TextField(max_length=500)
    designer = models.TextField(max_length=30)
    year_released = models.DateField()
    game_duration = models.IntegerField(max_length=5)
    number_of_players = models.IntegerField(max_length=5)
    age_reccommendation = models.IntegerField(max_length=3)
    category = models.ManyToManyField("Category", through="GameCategory" ,related_name="game_type")
    rating = models.ManyToManyField("Player", through='GameRating', related_name="rated")
    host = models.ForeignKey("Player", on_delete=models.CASCADE)
    
    def rater_check(self, rater):
        ratings = GameRating.objects.filter(game=self)
        return rater in ratings
    @property
    def rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRating.objects.filter(game=self)
        if len(ratings) == 0:
            return "This Game Has No Ratings"
        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        
        return total_rating / len(ratings)
        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.
