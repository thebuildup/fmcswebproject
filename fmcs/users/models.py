from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import re


def validate_twitter(value):
    if not value.startswith('https://twitter.com/'):
        raise ValidationError("Twitter username must start with 'https://twitter.com/'")


def validate_telegram(value):
    if not value.startswith('https://t.me/'):
        raise ValidationError("Telegram username must start with 'https://t.me/'")


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars/',
                               default='avatars/default.jpg',
                               blank=True, null=True)
    country = CountryField(countries_flag_url="//flagcdn.com/32x24/{code}.png", default=None, blank=True, null=True)
    twitter = models.CharField(max_length=100, default=None, blank=True, null=True)
    discord = models.CharField(max_length=100, default=None, blank=True, null=True)
    telegram = models.CharField(max_length=100, default=None, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
