from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import GameBoard, Histories, init_board


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', )

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
        # fields = ['id', 'owner', 'winner', 'queue', 'players', 'board', 'board_length', 'histories']

    def create(self, validated_data):
        print(validated_data)
        board = GameBoard(**validated_data)
        board.save()
        board.players.add(validated_data["owner"])
        return board
        # return Histories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(instance, validated_data)
        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)
        # instance.save()
        return instance


class GameBoardPlayersSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameBoard
        fields = ('players', )

    def update(self, instance, validated_data):
        print(instance, validated_data)

        return instance


class GameBoardStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Histories
        fields = ('step', )

    def create(self, validated_data):
        print(validated_data)
        return Histories(**validated_data)

    def update(self, instance, validated_data):
        Histories.objects.create(
            game_board=instance,
            step_by=instance.queue,
            board=instance.board,
            step=validated_data.get('step', [1, 2]),
            order=len(instance.histories.all())
        )

        instance.board = validated_data.get('board', instance.board)
        instance.queue = validated_data.get('queue', instance.queue)

        # instance.winner = validated_data.get('winner', instance.winner)
        # instance.ended = validated_data.get('ended', instance.ended)
        instance.is_ended = validated_data.get('is_ended', instance.is_ended)

        return instance