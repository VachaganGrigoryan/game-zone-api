from django.contrib import admin
from .models import GameBoard, Histories


@admin.register(GameBoard)
class GameBoardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'winner', 'created', 'is_ended')



@admin.register(Histories)
class HistoriesAdmin(admin.ModelAdmin):
    list_display = ('game_board', 'board', 'step', 'step_by', 'step_date')
