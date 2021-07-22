from rest_framework import permissions
from .models import GameBoard


class IsPlayerUser(permissions.BasePermission):
    message = 'The user is not player!'

    # def has_permission(self, request, view):
    #     blocked = GameBoard.objects.filter(pk=12).first()
    #     return request.user in blocked.players.all()

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return request.user in obj.players.all()


class IsPlayerTurn(permissions.BasePermission):
    message = 'It is not the player\'s turn!'

    # def has_permission(self, request, view):
    #     blocked = GameBoard.objects.filter(pk=12).first()
    #     return request.user in blocked.players.all()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.queue


class IsGameBoardFull(permissions.BasePermission):
    message = 'The Game Board is full!'

    def has_object_permission(self, request, view, obj):
        return obj.is_full
