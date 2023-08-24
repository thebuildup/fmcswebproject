import re
from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from glicko.models import Player, Match
from engine.models import Tournament, Participant, Organizator


class Command(BaseCommand):
    help = 'Imports data from pgn file and saves to Match table.'

    def add_arguments(self, parser):
        parser.add_argument('pgn_file', type=str, help='Path to the pgn file.')
        parser.add_argument('user_id', type=int, help='User ID for confirmation.')
        parser.add_argument('org_id', type=int, help='User ID for confirmation.')

    def handle(self, *args, **kwargs):
        pgn_file_path = kwargs['pgn_file']
        user_id = kwargs['user_id']
        org_id = kwargs['org_id']

        user = User.objects.get(id=user_id)
        org = Organizator.objects.get(id=org_id)

        with open(pgn_file_path, 'r') as pgn_file:
            pgn_data = pgn_file.read()

            match_entries = re.split(r'\n\n', pgn_data)

            last_match_date = None

            for entry in match_entries:
                player_a_match = re.search(r'\[Player A "(.*?)"\]', entry)
                if player_a_match:
                    player_a = player_a_match.group(1)
                else:
                    player_a = None

                player_b_match = re.search(r'\[Player B "(.*?)"\]', entry)  # Исправлено здесь
                if player_b_match:
                    player_b = player_b_match.group(1)
                else:
                    player_b = None

                result1_match = re.search(r'\[Result1 "(.*?)"\]', entry)
                if result1_match:
                    result1 = result1_match.group(1)
                    if "-" in result1:
                        result1 = "0-0" if result1 == "1/2-1/2" else result1
                        player1_goals_m1, player2_goals_m1 = map(int, result1.split('-'))
                    else:
                        player1_goals_m1, player2_goals_m1 = 0, 0
                else:
                    player1_goals_m1, player2_goals_m1 = 0, 0

                result2_match = re.search(r'\[Result2 "(.*?)"\]', entry)  # Исправлено здесь
                if result2_match:
                    result2 = result2_match.group(1)
                    if "-" in result2:
                        result2 = "0-0" if result2 == "1/2-1/2" else result2
                        player1_goals_m2, player2_goals_m2 = map(int, result2.split('-'))
                    else:
                        player1_goals_m2, player2_goals_m2 = 0, 0
                else:
                    player1_goals_m2, player2_goals_m2 = 0, 0

                date_match = re.search(r'\[Date "(.*?)"\]', entry)
                if date_match:
                    date_str = date_match.group(1)
                    # Преобразование строки в формат datetime
                    date_played = datetime.strptime(date_str, "%Y.%m.%d").date()

                    # Обновить дату последнего матча, если эта дата больше текущей
                    if last_match_date is None or date_played > last_match_date:
                        last_match_date = date_played
                else:
                    date_played = None

                player1, created1 = Player.objects.get_or_create(name=player_a)
                player2, created2 = Player.objects.get_or_create(name=player_b)

                # Ищем или создаем турнир события (Event)
                tournament_name_match = re.search(r'\[Event "(.*?)"\]', entry)
                if tournament_name_match:
                    tournament_name = tournament_name_match.group(1)
                    tournament, created = Tournament.objects.get_or_create(
                        name=tournament_name,
                        defaults={'start_date': date_played}
                    )
                    if created:
                        tournament.format = 'round_robin'  # Установите формат турнира по вашему усмотрению
                        tournament.org = org  # Установите организатора турнира
                        tournament.save()

                else:
                    tournament = None

                match = Match(
                    player1=player1,
                    player2=player2,
                    num_matches=2,
                    player1_goals_m1=player1_goals_m1,
                    player2_goals_m1=player2_goals_m1,
                    player1_goals_m2=player1_goals_m2,
                    player2_goals_m2=player2_goals_m2,
                    date_played=date_played,
                    event=tournament,
                    confirmed=user,  # Set as confirmed
                )
                match.save()

            # После завершения цикла по матчам, установите end_date для Tournament
            if last_match_date:
                tournament.end_date = last_match_date
                tournament.save()

        self.stdout.write(self.style.SUCCESS('Data imported from pgn file and saved to Match table.'))
