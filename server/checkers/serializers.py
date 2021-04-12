from rest_framework import serializers
from .models import GameBoard, Histories, init_board


# GameBoard serializer
class GameBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBoard
        fields = '__all__'
        # exclude = ['histories', 'board', 'created']

    def create(self, validated_data):
        board = GameBoard(
            owner=validated_data['owner'],
            queue=validated_data['queue'],
            histories=validated_data['histories'],
            board_length=validated_data['board_length'],
        )
        board.set_board(init_board(board.board_length))
        board.save()
        return board

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance


# Histories serializer
class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Histories
        fields = '__all__'
