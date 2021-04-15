from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import GameBoard, Histories, init_board


# Histories serializer
class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        fields = ['id', 'order', 'step', 'step_date']


# GameBoard serializer
class GameBoardSerializer(serializers.ModelSerializer):
    histories = HistoriesSerializer(many=True, read_only=True)

    class Meta:
        model = GameBoard
        fields = '__all__'

    def create(self, validated_data):
        board = GameBoard(**validated_data)
        board.save()
        board.players.set([validated_data["owner"]])
        return board

    # def update(self, instance, validated_data):
    #     instance.players.set(validated_data['players'])
    #     return instance
    #
    # def validate_players(self, players):
    #     if len(players) > 2:
    #         raise serializers.ValidationError({"board": "board is already is fulled."})
    #     return players


class GameBoardPlayersSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameBoard
        fields = ('id', 'players')

    def update(self, instance, validated_data):
        instance.players.set(validated_data['players'])
        return instance

    def validate_players(self, players):
        if len(players) > 2:
            raise serializers.ValidationError({"board": "board is already is fulled."})
        return players


class GameBoardStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Histories
        fields = ('step', )

    # def create(self, validated_data):
    #     return Histories(**validated_data)

    def update(self, instance, validated_data):
        Histories.objects.create(
            game_board=instance,
            step_by=instance.queue,
            board=instance.board,
            step=validated_data.get('step', [1, 2]),
            order=len(instance.histories.all())
        )

        # instance.board = validated_data.get('board', instance.board)
        # instance.queue = validated_data.get('queue', instance.queue)
        # instance.winner = validated_data.get('winner', instance.winner)
        # instance.ended = validated_data.get('ended', instance.ended)
        # instance.is_ended = validated_data.get('is_ended', instance.is_ended)
        instance.save()
        return instance