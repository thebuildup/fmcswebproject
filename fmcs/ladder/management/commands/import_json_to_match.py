# import json
# from datetime import datetime
# from django.utils.timezone import make_aware
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from ladder.models import Players, Matches
#
#
# class Command(BaseCommand):
#     help = 'Imports data from JSON file and saves to Match table.'
#
#     def add_arguments(self, parser):
#         parser.add_argument('json_file', type=str, help='Path to the JSON file.')
#         parser.add_argument('user_id', type=int, help='User ID for confirmation.')
#
#     def handle(self, *args, **kwargs):
#         json_file_path = kwargs['json_file']
#         user_id = kwargs['user_id']
#
#         user = User.objects.get(id=user_id)
#
#         with open(json_file_path, 'r') as json_file:
#             matches_data = json.load(json_file)
#
#             for match_data in matches_data:
#                 team_data = match_data.get("teams")
#                 if not team_data or len(team_data) != 2:
#                     # Skip the match if team data is missing or not in the expected format
#                     continue
#
#                 team_names = match_data.get("team_names")
#                 winner_index = match_data.get("winner")
#
#                 if not (team_names and winner_index is not None):
#                     # Skip the match if any required data is missing
#                     continue
#
#                 # Process team names string into player names
#                 player_names = [name.strip() for name in team_names]
#
#                 # Extract player data for both teams
#                 player_data_team1 = team_data[0][0]
#                 player_data_team2 = team_data[1][0]
#
#                 # Extract player IDs and names
#                 player_id_team1 = player_data_team1.get("id")
#                 player_id_team2 = player_data_team2.get("id")
#                 player_name_team1 = player_data_team1.get("name")
#                 player_name_team2 = player_data_team2.get("name")
#
#                 # Create or update players based on IDs
#                 player1, created1 = Players.objects.update_or_create(
#                     discord_id=player_id_team1,
#                     defaults={'name': player_name_team1}
#                 )
#                 player2, created2 = Players.objects.update_or_create(
#                     discord_id=player_id_team2,
#                     defaults={'name': player_name_team2}
#                 )
#
#                 # Process date string into datetime and make it aware of the timezone
#                 date_str = match_data.get("time")
#                 date_played = make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")) if date_str else None
#
#                 # Extract game_num
#                 game_num = match_data.get("game_num")
#
#                 # Check if the match with the same game_num already exists in the database
#                 if Matches.objects.filter(game_num=game_num).exists():
#                     self.stdout.write(self.style.SUCCESS(f'Match with game_num {game_num} already exists. Skipping.'))
#                     continue
#
#                     # Extract winner name based on winner index
#                 winner_name = player_names[winner_index]
#
#                 # Set goals and winner based on winner name
#                 player1_goals_m1 = 1 if winner_name == player_names[0] else 0
#                 player2_goals_m1 = 1 if winner_name == player_names[1] else 0
#
#                 # Create and save match
#                 match = Matches(
#                     player1=player1,
#                     player2=player2,
#                     num_matches=1,
#                     player1_goals_m1=player1_goals_m1,
#                     player2_goals_m1=player2_goals_m1,
#                     date_played=date_played,
#                     confirmed=user,  # Set as confirmed
#                     game_num=game_num,
#                 )
#                 match.save()
#
#         self.stdout.write(self.style.SUCCESS('Data imported from JSON file and saved to Match table.'))

import requests
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ladder.models import Players, Matches


class Command(BaseCommand):
    help = 'Imports data from API and saves to Match table.'

    # def add_arguments(self, parser):
    #     parser.add_argument('server_id', type=int, help='Server ID for API request.')
    #     parser.add_argument('user_id', type=int, help='User ID for confirmation.')

    def handle(self, *args, **kwargs):
        # server_id = kwargs['server_id']
        server_id = '981079170257944616'
        # user_id = kwargs['user_id']
        user_id = '2'

        user = User.objects.get(id=user_id)

        url = f'https://api.neatqueue.com/api/history/{server_id}'
        headers = {
            'Authorization': 'K--c2spnDdj51823tS3UrN8bJ2CMff6e'  # Замените YOUR_API_KEY на ваш ключ доступа
        }

        response = requests.get(url, headers=headers)

        # Проверка успешности запроса
        if response.status_code == 200:
            data = response.json()

            for match_data in data:
                game_num_str = match_data.get("game_num")

                try:
                    game_num = int(game_num_str)
                except ValueError:
                    # Пропустить матчи, у которых game_num не является целым числом
                    continue
                # Пропустить матчи с game_num < 8
                if game_num < 8:
                    continue

                team_data = match_data.get("teams")
                if not team_data or len(team_data) != 2:
                    # Skip the match if team data is missing or not in the expected format
                    continue

                team_names = match_data.get("team_names")
                winner_index = match_data.get("winner")

                if not (team_names and winner_index is not None):
                    # Skip the match if any required data is missing
                    continue

                # Process team names string into player names
                player_names = [name.strip() for name in team_names]

                # Extract player data for both teams
                player_data_team1 = team_data[0][0]
                player_data_team2 = team_data[1][0]

                # Extract player IDs and names
                player_id_team1 = player_data_team1.get("id")
                player_id_team2 = player_data_team2.get("id")
                player_name_team1 = player_data_team1.get("name")
                player_name_team2 = player_data_team2.get("name")

                # Create or update players based on IDs
                player1, created1 = Players.objects.update_or_create(
                    discord_id=player_id_team1,
                    defaults={'name': player_name_team1}
                )
                player2, created2 = Players.objects.update_or_create(
                    discord_id=player_id_team2,
                    defaults={'name': player_name_team2}
                )

                # Process date string into datetime and make it aware of the timezone
                date_str = match_data.get("time")
                date_played = make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")) if date_str else None

                # Extract game_num
                game_num = match_data.get("game_num")

                # Check if the match with the same game_num already exists in the database
                if Matches.objects.filter(game_num=game_num).exists():
                    self.stdout.write(self.style.SUCCESS(f'Match with game_num {game_num} already exists. Skipping.'))
                    continue

                # Extract winner name based on winner index
                winner_name = player_names[winner_index]

                # Set goals and winner based on winner name
                player1_goals_m1 = 1 if winner_name == player_names[0] else 0
                player2_goals_m1 = 1 if winner_name == player_names[1] else 0

                # Create and save match
                match = Matches(
                    player1=player1,
                    player2=player2,
                    num_matches=1,
                    player1_goals_m1=player1_goals_m1,
                    player2_goals_m1=player2_goals_m1,
                    date_played=date_played,
                    confirmed=user,  # Set as confirmed
                    game_num=game_num,
                )
                match.save()

            self.stdout.write(self.style.SUCCESS('Data imported from API and saved to Match table.'))
        else:
            print('Ошибка при выполнении запроса:', response.status_code)
