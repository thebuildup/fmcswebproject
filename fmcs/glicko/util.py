"""Helper functions."""

from datetime import timedelta

from django.conf import settings
from django.db import connection
from django.utils import timezone

from .models import Match, MatchupStatsNode, PlayerStatsNode, RatingPeriod, Player, PlayerRatingNode
from .ratings import calculate_new_rating_period

import csv


def glicko_reprocess_all_stats(reset_id_counter=True):
    print('Reprocess all stats')
    """Wipes all existing stats nodes and creates new stats nodes.

    Args:
        reset_id_counter: An optional boolean specifying whether to
            reset to ID counter for stats nodes back to 1.
    """
    # Wipe existing nodes
    PlayerStatsNode.objects.all().delete()
    MatchupStatsNode.objects.all().delete()

    # Reset ID counter
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE glicko_playerstatsnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE glicko_matchupstatsnode_id_seq RESTART with 1"
            )

    # Recreate nodes
    for game in Match.objects.order_by("date_played"):
        game.process_game()


def glicko_process_new_ratings():
    print('Process new ratings')
    """Calculates any new potential rating periods."""
    # Find first datetime where there exists unrated games. Recall that
    # rating periods and games are ordered from newest to oldest.
    latest_rating_period = RatingPeriod.objects.first()

    if latest_rating_period:
        start_datetime = (
                latest_rating_period.end_datetime + timedelta.resolution
        )
    else:
        # No rating periods. Use the date of the earliest game if one
        # exists; if no games exist, return.
        earliest_game = Match.objects.last()

        if not earliest_game:
            return

        start_datetime = earliest_game.date_played

    # Find out whether there's been enough time elapsed to make a new
    # rating period
    end_datetime = start_datetime + timedelta(
        days=settings.GLICKO2_RATING_PERIOD_DAYS
    )

    # Not enough time elapsed: return.
    if end_datetime > timezone.now():
        return

    # Calculate the new rating period and call this function again
    calculate_new_rating_period(start_datetime, end_datetime)
    print('Calculate completed')
    # Go again
    glicko_process_new_ratings()


def glicko_reprocess_all_ratings(reset_id_counter=True):
    print('Reprocess all ratings')
    """Wipes existing rating periods and rating nodes and creates new ones.

    Args:
        reset_id_counter: An optional boolean specifying whether to
            reset to ID counter for stats nodes back to 1.
    """
    # Wipe all existing rating periods and rating nodes. Note that
    # manually deleting player rating nodes isn't strictly necessary,
    # since they should all be deleted when their corresponding rating
    # periods are deleted.
    RatingPeriod.objects.all().delete()

    # Reset ID counter
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE glicko_playerratingnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE glicko_ratingperiod_id_seq RESTART with 1"
            )

    # Recalculate ratings
    glicko_process_new_ratings()


def clear_match_table():
    # Clear the Match table
    Match.objects.all().delete()


def clear_player_rating_node_table():
    try:
        PlayerRatingNode.objects.all().delete()
        print("Таблица PlayerRatingNode была успешно очищена.")
    except Exception as e:
        print("Произошла ошибка при очистке таблицы PlayerRatingNode:", str(e))


def clear_player_table(self):
    try:
        Player.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE glicko_player_id_seq RESTART WITH 1;")

        self.stdout.write(self.style.SUCCESS('Player table cleared, and IDs reset to start from 1.'))
    except Exception as e:
        print("Произошла ошибка при очистке таблицы Player:", str(e))


def clear_rating_period_table():
    try:
        RatingPeriod.objects.all().delete()
        print("Таблица RatingPeriod была успешно очищена.")
    except Exception as e:
        print("Произошла ошибка при очистке таблицы RatingPeriod:", str(e))


def import_csv_to_match(csv_file_path):
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            matches_to_create = []
            for row in reader:
                # Получаем данные из строки CSV
                player_a_name = row['Player A']
                # team_a = row['Team A']
                player_b_name = row['Player B']
                # team_b = row['Team B']
                result1 = row['Result1']
                result2 = row['Result2']
                date_played = row['Date']

                print(player_a_name)
                print(player_b_name)
                print(result1)
                print(result2)
                # print(player1_goals_m2)
                # print(player2_goals_m2)
                print(date_played)
                # Поиск или создание игроков Player A и Player B
                player_a, created_a = Player.objects.get_or_create(name=player_a_name)
                player_b, created_b = Player.objects.get_or_create(name=player_b_name)

                # Разбиваем результаты на голы
                player1_goals_m1, player2_goals_m1 = map(int, result1.split('-'))
                player1_goals_m2, player2_goals_m2 = map(int, result2.split('-'))

                match = Match.objects.create(
                    player1=player_a,
                    player2=player_b,
                    num_matches=2,
                    player1_goals_m1=player1_goals_m1,
                    player2_goals_m1=player2_goals_m1,
                    player1_goals_m2=player1_goals_m2,
                    player2_goals_m2=player2_goals_m2,
                    player1_goals_m3=None,
                    player2_goals_m3=None,
                    player1_goals_m4=None,
                    player2_goals_m4=None,
                    player1_goals_m5=None,
                    player2_goals_m5=None,
                    date_played=date_played,
                    confirmed=None,
                    rating_period=None,
                )
                match.save()

        print("Данные из CSV файла успешно импортированы в таблицу Match.")
    except Exception as e:
        print("Произошла ошибка при импорте данных из CSV файла:", str(e))
