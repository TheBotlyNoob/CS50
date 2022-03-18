from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by("-created_at")
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, "network/profile.html", {
        "given_user": user
    })


@login_required
def following(request):
    return render(request, "network/index.html", {
        "posts": map(lambda user: user.posts.order_by("-created_at"), request.user.followed_users.all())
    })


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post(user=request.user, content=content)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new-post.html")


@login_required
def follow(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = User.objects.get(id=id)
        if request.user == user:
            return HttpResponse("You cannot follow yourself.", status_code=400)

        request.user.followed_users.add(user)
        return HttpResponseRedirect(reverse("following"))
    else:
        return HttpResponseRedirect(reverse("index"), status_code=400)
