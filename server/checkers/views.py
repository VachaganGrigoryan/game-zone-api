from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from .models import GameBoard
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
        for item in request:
            print(request[item])

        return Response({})

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