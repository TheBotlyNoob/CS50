# Generated by Django 4.0.3 on 2022-03-15 20:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listing_current_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]