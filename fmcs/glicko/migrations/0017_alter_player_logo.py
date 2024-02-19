# Generated by Django 4.2.2 on 2023-12-05 08:51

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('glicko', '0016_alter_player_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='logo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='media/team_logos/logo_fmcs.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[1920, 1080], upload_to='media/team_logos/'),
        ),
    ]
