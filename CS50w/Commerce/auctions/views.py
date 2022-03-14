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
from .forms import ListingForm, SearchForm


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


def search(request):
    search_form = SearchForm(request.GET)

    if not search_form.is_valid():
        return render(request, "auctions/search.html", {
            "message": "Invalid search query."
        })

    search = search_form.cleaned_data

    if not search.get("category") and not search.get("title"):
        return render(request, "auctions/search.html", {
            "form": search_form,
        })

    found = Listing.objects.filter(active=True)

    if search.get("category"):
        found = found.filter(category=search.get("category"))

    if search.get("title"):
        found = found.filter(title__contains=search.get("title"))

    return render(request, "auctions/search.html", {
        "listings": found,
        "category": search.get("category"),
        "title": search.get("title"),
    })


@ login_required
def new_listing(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            listing: Listing = listing_form.save(commit=False)
            listing.user = request.user
            listing.starting_time = make_aware(datetime.now())
            listing.current_bid = listing.starting_bid

            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        else:
            return render(request, "auctions/new_listing.html", {"categories": Category.objects.all(), "form": listing_form, "message": "Invalid data"})
    else:
        return render(request, "auctions/new_listing.html", {"categories": Category.objects.all(), "form": ListingForm()})
