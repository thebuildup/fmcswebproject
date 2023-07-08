from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a new event')

    def __str__(self):
        return self.name
