from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    liked_posts = models.ManyToManyField(
        "Post", related_name="liked", blank=True)
    followed_users = models.ManyToManyField(
        "self", related_name="users_following", blank=True, symmetrical=False)

    def serialize_for_post(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "followed_users": [p.serialize() for p in self.followed_users.all()],
            "liked_posts": [p.serialize() for p in self.liked_posts.all()],
        }


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "liked": list(map(lambda user: user.serialize_for_post(), self.liked.all())),
        }
