# Generated by Django 4.0.3 on 2022-03-20 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0002_user_dir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='dir',
        ),
    ]
