# Generated by Django 4.2.2 on 2023-06-16 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("team_name", models.CharField(max_length=30)),
                ("ranking", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
