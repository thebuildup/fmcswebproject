from django.utils import timezone
from django.db.models import Q
from . import models
from . import glicko2
from django.conf import settings
import math


def calculate_new_rating_period(start_datetime, end_datetime):
    print("calc new rating period")
    # Создаём рейтинговый период или получите существующий
    rating_period, _ = models.RatingPeriod.objects.get_or_create(
        start_datetime=start_datetime, end_datetime=end_datetime
    )

    # Получаем все игры в этот рейтинговый период
    games = models.Match.objects.filter(
        date_played__gte=start_datetime, date_played__lte=end_datetime
    )
    # num_matches = models.Match.num_matches

    # Отметить все вышеперечисленные игры как принадлежащие этому рейтинговому периоду.
    for game in games:
        game.rating_period = rating_period
        game.save()

    # Для каждого игрока найдите все его матчи и их результаты в этих матчах; затем подсчитайте их рейтинги.
    # Словарь new_ratings содержит игроков в качестве ключей, а словари, содержащие их новые параметры рейтинга,
    # в качестве значений словаря.
    new_ratings = {}
    new_player_ratings = []
    num_matches = models.Match.objects.first().num_matches
    # players = models.Player.objects.all()

    for player in models.Player.objects.all():
        # Получить все игры, сыгранные игроком за этот рейтинговый период.
        # games_played_by_player = games.filter(Q(player1=player) | Q(player2=player))
        first_game_played = player.get_first_game_played()
        # If the player didn't play in this rating period, update inactivity
        if (
                first_game_played is None
                or first_game_played.date_played > end_datetime
        ):
            continue

        # Игрок, игравший в этом рейтинговом периоде
        # Получить параметры рейтинга игроков
        player_rating = player.rating
        player_rating_deviation = player.rating_deviation
        player_inactivity = player.inactivity
        player_rating_volatility = player.rating_volatility

        opponent_ratings = []
        opponent_rating_deviations = []
        scores = []

        for i in range(1, num_matches + 1):
            for game in games.filter(Q(player1=player) | Q(player2=player)):
                if game.is_winner(player, i):
                    scores.append(1.0)
                elif game.is_loser(player, i):
                    scores.append(0.0)
                else:
                    scores.append(0.5)

                if game.player1 == player:
                    opponent_ratings.append(game.player2.rating)
                    opponent_rating_deviations.append(game.player2.rating_deviation)
                elif game.player2 == player:
                    opponent_ratings.append(game.player1.rating)
                    opponent_rating_deviations.append(game.player1.rating_deviation)

                print('Цикл game filter')
                print(opponent_ratings)

            if not opponent_ratings:
                opponent_ratings = None
                opponent_rating_deviations = None
                scores = None

            print('Перед запуском расчётов')
            print(opponent_ratings)
            # Glicko-2
            new_player_rating, new_player_rating_deviation, new_player_rating_volatility = glicko2.calculate_player_rating(
                r=player_rating,
                RD=player_rating_deviation,
                sigma=player_rating_volatility,
                opponent_rs=opponent_ratings,
                opponent_RDs=opponent_rating_deviations,
                scores=scores,
            )
            new_player_ratings.append(new_player_rating)

        if new_player_ratings:
            average_new_player_rating = sum(new_player_ratings) / len(new_player_ratings)
        else:
            # Обработка случая, когда ни один игрок не сыграл ни одного матча за рейтинговый период.
            average_new_player_rating = 0.0
        print('Перед проверкой')
        print(opponent_ratings)
        # Рассчитать новое бездействие
        if opponent_ratings is None:
            new_player_inactivity = player_inactivity + 1
            new_player_rating_deviation = ((700 - 2 * new_player_rating_deviation) *
                                           ((math.atan(new_player_inactivity * 30 / 90)) / math.pi)
                                           + new_player_rating_deviation)
        else:
            new_player_inactivity = 0

        # Определите, помечен ли игрок как активный
        new_player_is_active = bool(
            new_player_inactivity
            < settings.NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE
        )

        new_ratings[player] = {
            "player_ranking": None,
            "player_ranking_delta": None,
            "player_rating": new_player_rating,
            "player_rating_deviation": new_player_rating_deviation,
            "player_rating_volatility": new_player_rating_volatility,
            "player_inactivity": new_player_inactivity,
            "player_is_active": new_player_is_active,
        }

    # Фильтровать всех активных игроков и сортировать по рейтингу
    new_active_player_ratings = [
        (player, new_rating["player_rating"])
        for player, new_rating in new_ratings.items()
        if new_rating["player_is_active"]
    ]
    new_active_player_ratings.sort(key=lambda x: x[1], reverse=True)

    # Обрабатывать новые рейтинги и изменения в рейтингах
    num_active_players = len(new_active_player_ratings)

    # Отслеживайте целочисленный рейтинг предыдущего игрока для определения равенства в рейтинге.
    last_integer_rating = None
    last_ranking = None

    for idx, player_tuple in enumerate(new_active_player_ratings, 1):
        # Распакуйте кортеж игрока
        player, rating = player_tuple
        integer_rating = round(rating)

        if (
                last_integer_rating is not None
                and last_integer_rating == integer_rating
        ):
            ranking = last_ranking
        else:
            last_integer_rating = integer_rating
            last_ranking = idx
            ranking = idx

        # Рейтинг
        new_ratings[player]["player_ranking"] = ranking

        # Дельта рейтинга
        if player.ranking is None:
            new_ratings[player]["player_ranking_delta"] = (
                    num_active_players - ranking + 1
            )
        else:
            new_ratings[player]["player_ranking_delta"] = (
                    player.ranking - ranking
            )

    # Теперь сохраняем все рейтинги
    for player, ratings_dict in new_ratings.items():
        models.PlayerRatingNode.objects.create(
            player=player,
            rating_period=rating_period,
            ranking=ratings_dict["player_ranking"],
            ranking_delta=ratings_dict["player_ranking_delta"],
            rating=ratings_dict["player_rating"],
            rating_deviation=ratings_dict["player_rating_deviation"],
            rating_volatility=ratings_dict["player_rating_volatility"],
            inactivity=ratings_dict["player_inactivity"],
            is_active=ratings_dict["player_is_active"],
        )

    # return
