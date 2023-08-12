from django.core.management.base import BaseCommand
from glicko.util import clear_player_table


class Command(BaseCommand):
    help = 'Clears the Player table in the database.'

    def handle(self, *args, **kwargs):
        clear_player_table(self)
