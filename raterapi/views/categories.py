from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Games, Player, GameReviews, Category


class CategoriesView(ViewSet):
    def list(self,request):
        cats = Category.objects.all()
        data = CatSerializer(cats, many=True, context={'request': request})
        return Response(data.data)

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label',)