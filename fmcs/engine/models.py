from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


class Organizator(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_tournaments_count(self):
        return self.tournaments.count()  # Подсчет турниров для каждого организатора


# Create your models here.
class Tournament(models.Model):
    FORMAT_CHOICES = (
        ('single_elimination', 'Single Elimination'),
        ('double_elimination', 'Double Elimination'),
        ('round_robin', 'Round Robin'),
        ('swiss', 'Swiss System'),  # Добавляем швейцарскую систему
    )

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    swiss_rounds = models.PositiveIntegerField(default=0)  # Количество раундов для швейцарской системы
    org = models.ForeignKey(Organizator, on_delete=models.SET_NULL, null=True, blank=True, related_name='tournaments')

    # Другие поля, которые могут понадобиться

    def __str__(self):
        return self.name

    def get_status(self):
        today = date.today()
        if self.end_date and today > self.end_date:
            return "Finished"
        elif today < self.start_date:
            return "Upcoming"
        else:
            return "Ongoing"


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)

    # Другие поля, которые могут понадобиться

    def __str__(self):
        return self.name

    def clean(self):
        if self.tournament_id and self.tournament.format == 'single_elimination' and self.pk:
            raise ValidationError("You cannot add participants to a Single Elimination tournament once it has started.")
