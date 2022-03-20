from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class ExecutedCommand(models.Model):
    command = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="command_history")

    def __str__(self):
        return self.command
