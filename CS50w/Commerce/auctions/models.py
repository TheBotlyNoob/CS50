from django.contrib.auth.models import AbstractUser
from django.db.models import *
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Category(Model):
    name = CharField(max_length=50, unique=True)
    description = CharField(max_length=200)

    def __str__(self):
        return self.name


class Bid(Model):
    amount = FloatField(validators=[MinValueValidator(0.01)])


class Listing(Model):
    title = CharField(max_length=50)
    description = CharField(
        max_length=200, default="")
    category = ForeignKey(
        Category, on_delete=CASCADE)
    image_url = URLField(
        default="https://via.placeholder.com/250x250.png?text=No+Image", editable=True)
    user = ForeignKey(User, on_delete=CASCADE)
    starting_bid = FloatField(validators=[MinValueValidator(0.01)])
    current_bid = PositiveIntegerField()
    starting_time = DateTimeField()
    ending_time = DateTimeField()
    active = BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - Highest Bid: {self.current_bid}"
