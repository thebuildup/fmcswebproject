"""Пользовательская команда для повторной обработки всех оценок."""

from django.core.management.base import BaseCommand
# from api.util import reprocess_all_ratings
from ladder.util import ladder_reprocess_all_ratings


class Command(BaseCommand):
    help = "Wipes all rating nodes and rating periods and recreates/recalculates them"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-id-counter",
            action="store_true",
            help="Reset ID counter back to 1 before recreating stats nodes.",
        )

    def handle(self, *args, **options):
        ladder_reprocess_all_ratings(reset_id_counter=options["reset_id_counter"])
