from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import make_aware

from datetime import datetime

from .models import User, Listing, Category, Bid, Comment
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
        current_bid = listing.bids.latest("amount")
        message = None
    except Listing.DoesNotExist:
        listing = None
        current_bid = None
        message = "Listing does not exist."

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "current_bid": current_bid,
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


@login_required
def new_listing(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            listing: Listing = listing_form.save(commit=False)
            listing.user = request.user
            listing.starting_time = make_aware(datetime.now())

            if listing.image_url == "" or listing.image_url is None:
                listing.image_url = "https://via.placeholder.com/250.png?text=No+Image"

            listing.save()

            Bid(amount=listing_form.cleaned_data["starting_bid"],
                listing=listing, user=request.user).save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        else:
            return render(request, "auctions/new_listing.html", {"categories": Category.objects.all(), "form": listing_form, "message": "Invalid data."})
    else:
        return render(request, "auctions/new_listing.html", {"categories": Category.objects.all(), "form": ListingForm()})


@login_required
def bid(request, id):
    if request.method == "POST":
        amount = request.POST["bid"]

        try:
            listing: Listing = Listing.objects.get(id=id)
        except Listing.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "message": "Listing does not exist."
            })

        if not listing.active:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Listing is no longer active."
            })

        try:
            amount = float(amount)
        except ValueError:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid amount must be a number."
            })

        if amount > 0.01:
            if listing.bids.latest("amount").amount < amount:
                Bid(user=request.user, listing=listing,
                    amount=amount).save()

                return HttpResponseRedirect(reverse("listing", args=(id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Bid amount must be greater than current price."
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid amount must be greater than 0.01."
            })
    else:
        return render(request, "auctions/listing.html", {
            "message": "Bid must be POSTed."
        })


def watchlist(request):
    if request.method == "POST":
        try:
            listing_id = int(request.POST["listing_id"])
        except:
            return render(request, "auctions/watchlist.html", {
                "message": "Invalid data."
            })

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return render(request, "auctions/watchlist.html", {
                "message": "Listing does not exist."
            })

        if listing.active:
            request.user.watchlist.add(listing)

            return HttpResponseRedirect(reverse("watchlist"))

        else:
            return render(request, "auctions/watchlist.html", {
                "message": "Listing is no longer active."
            })
    else:
        if request.user.is_authenticated:
            return render(request, "auctions/watchlist.html", {
                "listings": request.user.watchlist.all()
            })
        else:
            return render(request, "auctions/watchlist.html", {
                "message": "You must be logged in to view your watchlist."
            })


def comment(request, id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=id)
        except Listing.DoesNotExist:
            return render(request, "auctions/listing.html", {
                "message": "Listing does not exist."
            })

        try:
            comment = request.POST["comment"]
        except:
            return render(request, "auctions/listing.html", {
                "message": "Invalid data."
            })

        Comment(user=request.user, listing=listing, text=comment).save()

        return HttpResponseRedirect(reverse("listing", args=(id,)))

    else:
        return render(request, "auctions/listing.html", {
            "message": "Comment must be POSTed."
        })
