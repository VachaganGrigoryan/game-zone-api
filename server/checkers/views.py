from uuid import uuid4

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from .permissions import IsPlayerUser, IsPlayerTurn, IsGameBoardFull
from .models import GameBoard, init_board
from .serializers import GameBoardSerializer, GameBoardStepSerializer, GameBoardPlayersSerializer, \
    GameBoardDetailsSerializer


class GameBoardViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = GameBoard.objects.all()
    serializer_class = GameBoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsPlayerUser, IsPlayerTurn)

    @staticmethod
    def get_object(uuid):
        try:
            return GameBoard.objects.get(uuid=uuid)
        except GameBoard.DoesNotExist:
            raise Http404

    def list(self, request):
        game_boards = GameBoard.objects.all()
        serializer = self.serializer_class(game_boards, many=True)
        return Response(serializer.data)

    def create(self, request):
        data: dict = request.data
        current_user_id = request.user.id
        data.update({
            'uuid': str(uuid4()).upper(),
            'owner': current_user_id,
            'queue': current_user_id,
            'board': init_board(data.get('board_length', 8))
        })
        serializer = self.serializer_class(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, uuid=None):
        game_board = self.get_object(uuid=uuid)
        self.check_object_permissions(request, game_board)
        serializer = GameBoardDetailsSerializer(game_board)
        return Response(serializer.data)

    def update(self, request, uuid=None):
        game_board = self.get_object(uuid=uuid)
        self.check_object_permissions(request, game_board)
        serializer = GameBoardStepSerializer(game_board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serializer_class(game_board).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, uuid=None):
        game_board = self.get_object(uuid=uuid)
        data = {
            'uuid': uuid,
            'players': list(*zip(*game_board.players.values_list('id'))) + [request.user.id],
        }
        serializer = GameBoardPlayersSerializer(game_board, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, uuid=None):
        game_board = self.get_object(uuid=uuid)
        game_board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
