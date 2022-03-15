from django.contrib import admin

from .models import *


class ListingAdmin(admin.ModelAdmin):
    list_filter = ('active',)


# Register your models here.
for model, model_admin in [(Listing, ListingAdmin)]:
    admin.site.register(model, model_admin)

for model in [User, Category, Bid, Comment]:
    admin.site.register(model)
