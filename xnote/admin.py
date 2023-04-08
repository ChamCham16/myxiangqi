from django.contrib import admin
from .models import Note, XiangqiGame, OpeningBookPlayedByMasters

# Register your models here.

admin.site.register(Note)
admin.site.register(XiangqiGame)
admin.site.register(OpeningBookPlayedByMasters)