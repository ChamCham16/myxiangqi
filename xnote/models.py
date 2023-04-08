from django.db import models
from users.models import User

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class XiangqiGame(models.Model):
    GAMEID = models.CharField(max_length=255)
    EVENT = models.CharField(max_length=255, null=True)
    DATE = models.CharField(max_length=255, null=True)
    ROUND = models.CharField(max_length=255, null=True)
    RESULT = models.CharField(max_length=255, null=True)
    REDPLAYER = models.CharField(max_length=255, null=True)
    REDCLUB = models.CharField(max_length=255, null=True)
    BLACKPLAYER = models.CharField(max_length=255, null=True)
    BLACKCLUB = models.CharField(max_length=255, null=True)
    OPENING = models.CharField(max_length=255, null=True)
    VARIATION = models.CharField(max_length=255, null=True)
    GAME = models.TextField(null=True)

    def __str__(self):
        return self.GAMEID
    
class OpeningBookPlayedByMasters(models.Model):
    move_number = models.IntegerField()
    fen = models.TextField()
    move = models.CharField(max_length=5)
    games = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    losses = models.IntegerField()

    def __str__(self):
        return self.fen