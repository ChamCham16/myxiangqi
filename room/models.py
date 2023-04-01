from django.db import models

# Create your models here.

class XiangqiRoom(models.Model):
    # only name and slug are required
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    white = models.CharField(max_length=255, blank=True)
    black = models.CharField(max_length=255, blank=True)
    white_name = models.CharField(max_length=255, blank=True)
    black_name = models.CharField(max_length=255, blank=True)
    turn = models.CharField(max_length=255, blank=True)
    board = models.CharField(max_length=255, blank=True)
    winner = models.CharField(max_length=255, blank=True)
    white_ready = models.BooleanField(default=False)
    black_ready = models.BooleanField(default=False)

    def __str__(self):
        return self.name