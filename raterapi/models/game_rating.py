from django.db import models

class GameRating(models.Model):
    game = models.ForeignKey("Games", on_delete= models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=2)