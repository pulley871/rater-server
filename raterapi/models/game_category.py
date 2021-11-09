from django.db import models

class GameCategory(models.Model):
    game = models.ForeignKey('Games', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)