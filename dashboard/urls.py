from django.urls import path, include
from .views import DashBoardViewSet

dashboard = DashBoardViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path("", dashboard, name="game-board-list"),
]
