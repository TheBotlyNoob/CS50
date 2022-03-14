from tracemalloc import start
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import make_aware

from datetime import datetime

from .models import User, Listing, Category


def index(request):
    return render(request, "auctions/index.html", {"active_listings": Listing.objects.filter(active=True)})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, id):
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        listing = None

    return render(request, "auctions/listing.html", {
        "listing": listing
    })


@login_required
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        try:
            description = request.POST["description"]
        except KeyError:
            description = ""

        category = Category.objects.get(id=request.POST["category"])

        try:
            image = request.FILES["image"]
        except KeyError:
            image = ""

        starting_bid = int(request.POST["starting_bid"])

        ending_time = request.POST["end_time"]
        ending_date = request.POST["end_date"]

        ending_year = int(ending_date[0:4])
        ending_month = int(ending_date[5:7])
        ending_day = int(ending_date[8:10])

        ending_hour = int(ending_time[0:2])
        ending_minute = int(ending_time[3:5])

        ending = make_aware(datetime(ending_year, ending_month,
                                     ending_day, ending_hour, ending_minute))

        new_listing = Listing(title=title, description=description, category=category, image=image,
                              starting_bid=starting_bid, current_bid=starting_bid, starting_time=make_aware(
                                  datetime.now()),
                              ending_time=ending, user=request.user)

        new_listing.save()

        return HttpResponseRedirect(reverse("listing", args=(new_listing.id,)))
    else:
        return render(request, "auctions/new_listing.html", {"categories": Category.objects.all()})
