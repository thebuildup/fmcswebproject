# Generated by Django 4.2.2 on 2023-07-28 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("leaderboard", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="event",
        ),
    ]
