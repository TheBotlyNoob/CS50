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


class Comment(Model):
    text = CharField(max_length=200)
    user = ForeignKey(User, on_delete=CASCADE)
    listing = ForeignKey("Listing", on_delete=CASCADE)

    def __str__(self):
        return self.text


class Bid(Model):
    amount = FloatField(validators=[MinValueValidator(0.01)])
    user = ForeignKey(User, on_delete=CASCADE)
    listing = ForeignKey("Listing", on_delete=CASCADE, related_name="bids")

    def __str__(self):
        return str(self.amount)


class Listing(Model):
    title = CharField(max_length=50)
    description = CharField(
        max_length=200, default="")
    category = ForeignKey(
        Category, on_delete=CASCADE)
    image_url = URLField(
        default="https://via.placeholder.com/250x250.png?text=No+Image")
    user = ForeignKey(User, on_delete=CASCADE)
    starting_time = DateTimeField()
    ending_time = DateTimeField()
    active = BooleanField(default=True)
    watchlist = ManyToManyField(User, related_name="watchlist")

    def __str__(self):
        return f"{self.title} - Highest Bid: {self.bids.latest('amount')}"
