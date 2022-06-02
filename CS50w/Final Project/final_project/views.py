from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from asgiref.sync import sync_to_async

from tempfile import gettempdir
from shutil import rmtree

import re

from .models import *
import subprocess
import os

# Create your views here.


@login_required
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "login.html", {"message": "Invalid email and/or password."}
            )
    else:
        return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(
                request, "register.html", {"message": "Email address already taken."}
            )
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def execute(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "output": "Not logged in."})

        command: str = request.body.decode("utf-8")

        commands = list(command.split("&"))

        for command in commands:
            ExecutedCommand.objects.create(command=command, user=request.user).save()

        temp_dir = gettempdir() + "/online-terminal/" + str(request.user.id)

        os.makedirs(temp_dir, exist_ok=True)

        output = ""

        # very insecure, do not use in production
        for command in commands:
            try:
                output += (
                    subprocess.run(
                        command,
                        cwd=temp_dir,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        timeout=10,
                        shell=True,
                    )
                    .stdout.decode("utf-8")
                    .strip()
                    + "\n"
                )
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                print(e)
                output += (
                    "Command not found.\n"
                    if e is FileNotFoundError
                    else "Command timed out.\n"
                )

        return JsonResponse(
            {
                "success": True,
                "output": output,
                "command_history": [
                    command.command for command in request.user.command_history.all()
                ],
            }
        )
    else:
        return JsonResponse({"success": False, "output": "/execute should be POSTed"})


def command_history(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Not logged in."})

    return JsonResponse(
        {
            "success": True,
            "commands": [
                command.command for command in request.user.command_history.all()
            ],
        }
    )
