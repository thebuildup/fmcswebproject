from django.core.management.base import BaseCommand
from glicko.util import clear_player_rating_node_table


class Command(BaseCommand):
    help = 'Clears the PlayerRatingNode table in the database.'

    def handle(self, *args, **kwargs):
        clear_player_rating_node_table()
