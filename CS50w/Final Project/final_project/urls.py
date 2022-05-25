from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("execute", views.execute, name="execute"),
    path("command_history", views.command_history, name="command_history"),
]
