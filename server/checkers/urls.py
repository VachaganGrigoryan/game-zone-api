from django.urls import path, include
from .api import GameBoardApi, CreateApi, DeleteApi, FinishApi, JoinApi, ReadyApi, PlayApi, PauseApi

urlpatterns = [
    path("api/game-boards/", GameBoardApi.as_view(), name="game-boards"),
    path("api/game-boards/{pk}/", GameBoardApi.as_view(), name="game-board-detail"),
    # path("api/create", CreateApi.as_view(), name="create"),
    # path('api/delete', DeleteApi.as_view(), name="delete"),
    # path('api/finish', FinishApi.as_view(), name="finish"),
    # path('api/join', JoinApi.as_view(), name="join"),
    # path('api/ready', ReadyApi.as_view(), name="ready"),
    # path('api/play', PlayApi.as_view(), name="play"),
    # path('api/pause', PauseApi.as_view(), name="pause"),
]
