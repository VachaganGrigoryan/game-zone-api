from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import GameBoard, Histories, init_board


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'first_name', 'last_name', 'email', ]


# Histories serializer
class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        fields = '__all__'
        # fields = ['id', 'order', 'step', 'step_by', 'step_date']


# GameBoard serializer
class GameBoardSerializer(serializers.ModelSerializer):
    # histories = HistoriesSerializer(many=True, read_only=True)

    class Meta:
        model = GameBoard
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
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
        fields = ('uuid', 'players')

    def update(self, instance, validated_data):
        instance.players.set(validated_data['players'])
        # instance.is_full = False
        return instance

    def validate_players(self, players):
        print(players, self.fields)
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
            step=validated_data.get('step', []),
            order=instance.histories.count()
        )
        instance.queue = instance.players.filter(~Q(id=instance.queue.id)).first()
        # instance.board = validated_data.get('board', instance.board)
        # instance.queue = validated_data.get('queue', instance.queue)
        # instance.winner = validated_data.get('winner', instance.winner)
        # instance.ended = validated_data.get('ended', instance.ended)
        # instance.is_ended = validated_data.get('is_ended', instance.is_ended)
        instance.save()
        return instance

    def validate_is_full(self):
        print(players, self.fields)
        if len(players) > 2:
            raise serializers.ValidationError({"board": "board is already is fulled."})
        return


# GameBoard serializer
class GameBoardDetailsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    players = UserSerializer(many=True, read_only=True)
    histories = HistoriesSerializer(many=True, read_only=True)

    class Meta:
        model = GameBoard
        fields = '__all__'