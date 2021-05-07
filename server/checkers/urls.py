from django.urls import path, include
from .api import GameBoardApi, CreateApi, DeleteApi, FinishApi, JoinApi, ReadyApi, PlayApi, PauseApi
from .views import GameBoardViewSet

game_board_list = GameBoardViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
game_board_detail = GameBoardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
game_board_connect = GameBoardViewSet.as_view({
    'patch': 'partial_update',
})

urlpatterns = [
    path("game-boards/", game_board_list, name="game-board-list"),
    path("game-boards/<str:uuid>/", game_board_detail, name="game-board-detail"),
    path("game-boards/<str:uuid>/connect/", game_board_connect, name="game-board-connect"),
    # path("api/create", CreateApi.as_view(), name="create"),
    # path('api/delete', DeleteApi.as_view(), name="delete"),
    # path('api/finish', FinishApi.as_view(), name="finish"),
    # path('api/join', JoinApi.as_view(), name="join"),
    # path('api/ready', ReadyApi.as_view(), name="ready"),
    # path('api/play', PlayApi.as_view(), name="play"),
    # path('api/pause', PauseApi.as_view(), name="pause"),
]
