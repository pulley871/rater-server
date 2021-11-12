import uuid
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi import models
from raterapi.models import Games, Player, GameReviews, GamePicture
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from base64 import b64decode, b64encode
class GamePictureView(ViewSet):
    def create(self, request):
        # Create a new instance of the game picture model you defined
        # Example: game_picture = GamePicture()
        try:

            format, imgstr = request.data["game_image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}')
            GamePicture.objects.create(
                game = Games.objects.get(pk=request.data['game_id']),
                action_pic = data
            )
            return Response({}, status=status.HTTP_201_CREATED)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        pic = GamePicture.objects.get(pk=pk)
        
        serializer = ImageSer(pic, context={"request": request})
        return Response(serializer.data)






class ImageSer(serializers.ModelSerializer):
    class Meta:
        model = GamePicture
        fields = ("id", "game", "action_pic") 

        # Give the image property of your game picture instance a value
        # For example, if you named your property `action_pic`, then
        # you would specify the following code:
        #
        #       game_picture.action_pic = data

        # Save the data to the database with the save() method
