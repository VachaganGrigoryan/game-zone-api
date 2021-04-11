from django.contrib import admin
from .models import GameBoard, Histories


class GameBoardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'winner', 'board', 'created', 'is_ended')


class HistoriesAdmin(admin.ModelAdmin):
    list_display = ('board_id', 'board', 'step', 'step_by', 'step_date')


admin.site.register(GameBoard, GameBoardAdmin)
admin.site.register(Histories, HistoriesAdmin)