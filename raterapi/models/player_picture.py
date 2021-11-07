from django.db import models


class PlayerPicture(models.Model):
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    image_file = models.ImageField()