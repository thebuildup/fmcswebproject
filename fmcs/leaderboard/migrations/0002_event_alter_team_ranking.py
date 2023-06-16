# Generated by Django 4.2.2 on 2023-06-16 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leaderboard", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("event_name", models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name="team",
            name="ranking",
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
    ]
