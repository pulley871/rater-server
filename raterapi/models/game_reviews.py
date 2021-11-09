from django.db import models

class GameReviews(models.Model):
    game = models.ForeignKey("Games", on_delete=models.CASCADE, related_name='reviews')
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    description = models.TextField()
    