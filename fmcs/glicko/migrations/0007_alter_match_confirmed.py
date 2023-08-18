# Generated by Django 4.2.2 on 2023-08-18 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("glicko", "0006_rename_player1_goals_match_player1_goals_m1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="match",
            name="confirmed",
            field=models.ForeignKey(
                default=False,
                help_text="The user which submitted the game.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
