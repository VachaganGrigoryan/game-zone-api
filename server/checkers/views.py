from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from .models import GameBoard, init_board
from .serializers import GameBoardSerializer


class GameBoardViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    serializer_class = GameBoardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request):
        queryset = GameBoard.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data: dict = request.data.get("items") if 'items' in request.data else request.data
        current_user_id = request.user.id
        data.update({
            'owner': current_user_id,
            'queue': current_user_id,
            'board': init_board(data['board_length'])
        })
        many = isinstance(data, list)
        serializer = self.serializer_class(data=data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = GameBoard.objects.all()
        game_board = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(game_board)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass