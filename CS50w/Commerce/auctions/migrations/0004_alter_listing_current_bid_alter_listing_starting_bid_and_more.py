# Generated by Django 4.0.3 on 2022-03-14 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_listingcategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
