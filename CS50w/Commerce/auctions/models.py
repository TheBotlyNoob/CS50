from random import randint
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.PositiveIntegerField()
    current_bid = models.PositiveIntegerField()
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - Highest Bid: {self.current_bid}"
