from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


def init_board(length):
    if length not in [8, 10]:
        return ValueError("The Board should be have 8 or 10 length!")

    l_middle = length // 2

    def get_num(i, j):
        if i < l_middle - 1:
            return 2
        if i <= l_middle:
            return 1
        return 3

    return [[get_num(i, j) if (i + j) % 2 else 0 for j in range(length)] for i in range(length)]


class GameBoard(models.Model):
    class BoardLength(models.IntegerChoices):
        short = 8, 'Short'
        long = 10, 'Long'

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name='winner')
    queue = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name='queue')
    players = models.ManyToManyField(User, max_length=2, blank=True, related_name='players')
    histories = models.ManyToManyField('Histories', blank=True)
    board = ArrayField(ArrayField(models.IntegerField(blank=True, default=0)))
    board_length = models.IntegerField(choices=BoardLength.choices, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(blank=True)
    is_ended = models.BooleanField(default=False)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.__str__()


class Histories(models.Model):
    id = models.AutoField(primary_key=True)
    board_id = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name='game_board')
    board = ArrayField(ArrayField(models.IntegerField(blank=True, default=0)))
    step = ArrayField(models.IntegerField(blank=True))
    step_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    step_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.board_id.__str__()



