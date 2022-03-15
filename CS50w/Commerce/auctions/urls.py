from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("new", views.new_listing, name="new_listing"),
    path("search", views.search, name="search"),
    path("watchlist", views.watchlist, name="watchlist"),
]
