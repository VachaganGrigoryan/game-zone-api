from rest_framework import serializers
from .models import GameBoard, Histories


# GameBoard serializer
class GameBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBoard
        fields = '__all__'

    # extra_kwargs = {
    #     'password': {'write_only': True},
    # }


# Histories serializer
class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        fields = '__all__'
