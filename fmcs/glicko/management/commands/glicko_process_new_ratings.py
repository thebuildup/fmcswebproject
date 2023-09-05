"""Пользовательская команда для обработки нового рейтинга."""

from django.core.management.base import BaseCommand
# from .util import process_new_ratings
from glicko.util import glicko_process_new_ratings


class Command(BaseCommand):
    help = "Calculates and creates new rating nodes and rating periods"

    def handle(self, *args, **options):
        glicko_process_new_ratings()
