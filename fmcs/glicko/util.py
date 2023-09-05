"""Вспомогательные функции"""

from datetime import timedelta

from django.conf import settings
from django.db import connection
from django.utils import timezone

from .models import Match, MatchupStatsNode, PlayerStatsNode, RatingPeriod, Player, PlayerRatingNode
from .ratings import calculate_new_rating_period

import csv


def glicko_reprocess_all_stats(reset_id_counter=True):
    print('Reprocess all stats')
    """Удаление всей статистики и создание новой.
    """

    # Удаление всех записей статистики
    PlayerStatsNode.objects.all().delete()
    MatchupStatsNode.objects.all().delete()

    # Сброс ID
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE glicko_playerstatsnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE glicko_matchupstatsnode_id_seq RESTART with 1"
            )

    # Пересоздание статистики
    for game in Match.objects.order_by("date_played"):
        game.process_game()


def glicko_process_new_ratings():
    print('Process new ratings')
    """Calculates any new potential rating periods."""
    # Найдите первую дату и время, где существуют игры без рейтинга. Напомним, что
    # рейтинговых периодов и игр упорядочены от самых новых к самым старым.
    latest_rating_period = RatingPeriod.objects.first()

    if latest_rating_period:
        start_datetime = (
                latest_rating_period.end_datetime + timedelta.resolution
        )
    else:
        # Нет рейтинговых периодов. Используйте дату самой ранней игры, если она есть.
        # существует; если игр не существует, вернитесь.
        earliest_game = Match.objects.last()

        if not earliest_game:
            return

        start_datetime = earliest_game.date_played

    # Узнайте, прошло ли достаточно времени для создания нового
    # рейтинговый период
    end_datetime = start_datetime + timedelta(
        days=settings.GLICKO2_RATING_PERIOD_DAYS
    )

    # Прошло недостаточно времени: возврат.
    if end_datetime > timezone.now():
        return

    # Рассчитаем новый рейтинговый период и снова вызовем эту функцию
    calculate_new_rating_period(start_datetime, end_datetime)
    print('Calculate completed')
    # Еще раз
    glicko_process_new_ratings()


def glicko_reprocess_all_ratings(reset_id_counter=True):
    print('Reprocess all ratings')
    """Удаляет существующие рейтинговые периоды и рейтинговые записи и создает новые.
    """
    # Сотрите все существующие периоды рейтинга и записи рейтинга. Обратите внимание, что
    # удаление записей рейтинга игроков вручную не является строго необходимым,
    # так как все они должны быть удалены, когда их соответствующий рейтинговый
    # период удален.
    RatingPeriod.objects.all().delete()

    # Сбросить счетчик идентификаторов
    if reset_id_counter:
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE glicko_playerratingnode_id_seq RESTART with 1"
            )
            cursor.execute(
                "ALTER SEQUENCE glicko_ratingperiod_id_seq RESTART with 1"
            )

    # Пересчёт рейтинга
    glicko_process_new_ratings()


def clear_match_table():
    # Удаление таблицы матчей
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
