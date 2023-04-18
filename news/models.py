from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    popularity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Truth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='truths')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='truths')
    is_true = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Hashtag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    news = models.ManyToManyField(News, related_name='hashtags')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name