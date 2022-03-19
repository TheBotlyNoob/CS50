from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse

from .models import User, Post


def index(request):
    page = request.GET.get("page", 1)

    posts = Post.objects.order_by("-created_at")

    paginator = Paginator(posts, 10)

    page_obj = paginator.get_page(page)

    return render(request, "network/index.html", {
        "page_obj": page_obj
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
    page = request.GET.get("page", 1)

    posts = Post.objects.order_by("-created_at")

    paginator = Paginator(posts, 10)

    page_obj = paginator.get_page(page)

    return render(request, "network/profile.html", {
        "given_user": user,
        "page_obj": page_obj,
        "is_following": request.user in user.followed_users.all()
    })


@login_required
def following(request):
    page = request.GET.get("page", 1)

    posts = list()

    for user in request.user.users_following.all():
        posts += user.posts.order_by("-created_at")

    print(posts)

    paginator = Paginator(posts, 10)

    page_obj = paginator.get_page(page)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@ login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post(user=request.user, content=content)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new-post.html")


@ login_required
def follow(request):
    if request.method == "POST":
        id = request.POST["user_id"]
        user = User.objects.get(id=id)

        if request.user == user:
            return HttpResponse("You cannot follow yourself.", status_code=400)

        if request.user.users_following.filter(id=id).exists():
            print("a")
            request.user.users_following.remove(user)
        else:
            print("B")
            request.user.users_following.add(user)

        request.user.save()

        print(request.user.users_following.count())

        return JsonResponse({"success": True, "followers": request.user.users_following.count()})
    else:
        return HttpResponseRedirect(reverse("index"), status_code=400)


@ login_required
def edit(request):
    if request.method == "POST":
        content = request.POST["content"]
        post_id = int(request.POST["post_id"])

        post = Post.objects.get(id=post_id)
        if post.user != request.user:
            return JsonResponse({"error": "You cannot edit this post."}, status_code=400)

        post.content = content
        post.save()

        return JsonResponse({"post": post.serialize()})
    else:
        return HttpResponse("Method not allowed.", status_code=400)


@ login_required
def like_post(request):
    if request.method == "POST":
        post_id = int(request.POST["post_id"])
        post = Post.objects.get(id=post_id)

        if request.user.liked_posts.filter(id=post_id).exists():
            request.user.liked_posts.remove(post)
        else:
            request.user.liked_posts.add(post)

        request.user.save()

        print(request.user.liked_posts.all())

        return JsonResponse({"post": post.serialize()})
    else:
        return HttpResponse("Method not allowed.", status_code=400)
