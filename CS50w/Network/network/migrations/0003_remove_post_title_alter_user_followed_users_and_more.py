# Generated by Django 4.0.3 on 2022-03-17 23:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followed_users_post_user_liked_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AlterField(
            model_name='user',
            name='followed_users',
            field=models.ManyToManyField(
                blank=True, related_name='users_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(
                blank=True, related_name='liked', to='network.post'),
        ),
    ]
