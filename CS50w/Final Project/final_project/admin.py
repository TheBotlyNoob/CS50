from django.contrib import admin
from .models import User, ExecutedCommand

# Register your models here.

admin.site.register(User)
admin.site.register(ExecutedCommand)
