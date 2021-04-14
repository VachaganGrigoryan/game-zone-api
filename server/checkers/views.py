from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from .models import GameBoard, init_board
from .serializers import GameBoardSerializer, GameBoardStepSerializer, GameBoardPlayersSerializer


class GameBoardViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = GameBoard.objects.all()
    serializer_class = GameBoardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @staticmethod
    def get_object(pk):
        try:
            return GameBoard.objects.get(pk=pk)
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
            'owner': current_user_id,
            'queue': current_user_id,
            'board': init_board(data.get('board_length', 8))
        })
        many = isinstance(data, list)
        serializer = self.serializer_class(data=data, many=many)
        if serializer.is_valid():
            serializer.save()
            # serializer.players.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # game_boards = GameBoard.objects.all()
        # game_board = get_object_or_404(game_boards, pk=pk)
        game_board = self.get_object(pk=pk)
        serializer = self.serializer_class(game_board)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # game_board = GameBoard.objects.get(pk=pk)
        # game_boards = GameBoard.objects.all()
        # game_board = get_object_or_404(game_boards, pk=pk)
        game_board = self.get_object(pk=pk)
        serializer = GameBoardStepSerializer(game_board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serializer_class(game_board).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        game_board = self.get_object(pk=pk)
        serializer = GameBoardPlayersSerializer(game_board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serializer_class(game_board).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # game_board = GameBoard.objects.get(pk=pk)
        # game_boards = GameBoard.objects.all()
        # game_board = get_object_or_404(game_boards, pk=pk)
        game_board = self.get_object(pk=pk)
        game_board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def do_step(self, request, pk=None):
        game_board = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():

            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)