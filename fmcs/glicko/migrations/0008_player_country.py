# Generated by Django 4.2.2 on 2023-08-18 18:24

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glicko', '0007_alter_match_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default=None, max_length=2, null=True),
        ),
    ]