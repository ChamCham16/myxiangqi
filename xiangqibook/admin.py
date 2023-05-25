from django.contrib import admin
from .models import Book, XiangqiBook, XiangqiSection, XiangqiScript

# Register your models here.

admin.site.register(XiangqiBook)
admin.site.register(XiangqiSection)
admin.site.register(XiangqiScript)
admin.site.register(Book)