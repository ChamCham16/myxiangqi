from django.db import models
from users.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField(null=True)
    author = models.CharField(max_length=255, null=True)
    path = models.CharField(max_length=255, null=True)

    volume = models.CharField(max_length=255, null=True)
    chapter = models.CharField(max_length=255, null=True)
    section = models.CharField(max_length=255, null=True)
    game = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title
    
    # set author to the user's username
    def save(self, *args, **kwargs):
        self.author = self.user.username
        super(Book, self).save(*args, **kwargs)

class XiangqiBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)

    author = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.author = self.user.username
        super(XiangqiBook, self).save(*args, **kwargs)

class XiangqiSection(models.Model):
    book = models.ForeignKey(XiangqiBook, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=255)

    description = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class XiangqiScript(models.Model):
    section = models.ForeignKey(XiangqiSection, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
