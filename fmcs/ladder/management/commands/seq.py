from django.core.management.base import BaseCommand

# from glicko.util import clearmatchtable
from django.db import connection
from ladder.util import clear_match_table
from ladder.models import Matches


class Command(BaseCommand):
    help = 'Clears the Match table in the database and resets IDs to start from 1.'

    def handle(self, *args, **kwargs):
        # Clear the Match table

        # Reset IDs to start from 1 (only works for PostgreSQL)
        # The following SQL command sets the sequence for the "id" column in the "glicko_match" table
        # to start from 1, assuming the table name is "glicko_match".
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE glicko_match_id_seq RESTART WITH 583;")

        self.stdout.write(self.style.SUCCESS('IDs reset to start from 583.'))
