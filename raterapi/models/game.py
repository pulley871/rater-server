from django.db import models

from raterapi.models import category

class Games(models.Model):
    title = models.TextField(max_length=30)
    description = models.TextField(max_length=500)
    designer = models.ForeignKey("player", on_delete=models.CASCADE)
    year_released = models.DateField()
    game_duration = models.IntegerField(max_length=5)
    number_of_players = models.IntegerField(max_length=5)
    age_reccommendation = models.IntegerField(max_length=3)
    category = models.ManyToManyField("Category", through="GameCategory" ,related_name="game_type")
    rating = models.ManyToManyField("Player", through='GameRating', related_name="rated")