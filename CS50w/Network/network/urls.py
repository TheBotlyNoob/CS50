
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("new-post", views.new_post, name="new-post"),
    path("edit", views.edit, name="edit"),
    path("like", views.like_post, name="like"),
    path("follow", views.follow, name="follow"),
]
