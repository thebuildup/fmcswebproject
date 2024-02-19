from django.core.management.base import BaseCommand
from ladder.util import ladder_clear_player_table


class Command(BaseCommand):
    help = 'Clears the Player table in the database.'

    def handle(self, *args, **kwargs):
        ladder_clear_player_table(self)
