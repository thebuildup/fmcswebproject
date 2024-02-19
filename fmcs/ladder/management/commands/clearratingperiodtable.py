from django.core.management.base import BaseCommand
from glicko.util import clear_rating_period_table


class Command(BaseCommand):
    help = 'Clears the RatingPeriod table in the database.'

    def handle(self, *args, **kwargs):
        clear_rating_period_table()
