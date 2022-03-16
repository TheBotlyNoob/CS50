from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/comment", views.comment, name="comment"),
    path("listing/<int:id>/close", views.close, name="close"),
    path("non-active-listings", views.non_active_listings,
         name="non_active_listings"),
    path("new", views.new_listing, name="new_listing"),
    path("search", views.search, name="search"),
    path("watchlist", views.watchlist, name="watchlist"),
]
