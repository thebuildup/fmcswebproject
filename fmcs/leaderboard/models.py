from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    team_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    ranking = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def __str__(self):
        return self.team_name


class Status(models.Model):
    id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=15)

    def __str__(self):
        return self.status_name


class Organizator(models.Model):
    id = models.BigAutoField(primary_key=True)
    org_name = models.CharField(max_length=60)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.org_name


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=30)
    org_name = models.ForeignKey(Organizator, on_delete=models.SET_NULL, null=True, related_name='org')
    status_name = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.event_name


class Result(models.Model):
    match_id = models.BigAutoField(primary_key=True)
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team2')
    result = models.CharField(max_length=5)
    event_id = models.ForeignKey(Event, on_delete=models.PROTECT)
    match_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.
