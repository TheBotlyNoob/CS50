from django.contrib import admin

from .models import *

# Register your models here.
for model in [User, Category, Listing]:
    admin.site.register(model)
