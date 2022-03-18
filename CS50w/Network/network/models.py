from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    liked_posts = models.ManyToManyField(
        "Post", related_name="users_liked", blank=True)
    followed_users = models.ManyToManyField(
        "self", related_name="users_following", blank=True, symmetrical=False)


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
