from django.db import models
from .game import Games

class GamePicture(models.Model):
    game = models.ForeignKey(Games, on_delete=models.DO_NOTHING, related_name='pictures')
    action_pic = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
