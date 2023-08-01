from django.db.models import Q
from . import models
from . import glicko2
from django.conf import settings


def calculate_new_rating_period(start_datetime, end_datetime):
    print("calc new rating period")
    """Calculate a new ratings and a corresponding new rating period.

    Args:
        start_datetime: The datetime for the start of the rating period.
        end_datetime: The datetime for the end of the rating period.
    """
    # Create the rating period
    rating_period = models.RatingPeriod.objects.create(
        start_datetime=start_datetime, end_datetime=end_datetime
    )

    # Grab all games that will be in this rating period
    games = models.Match.objects.filter(
        date_played__gte=start_datetime, date_played__lte=end_datetime
    )

    # Mark all of the above games as belonging in this rating period
    for game in games:
        game.rating_period = rating_period
        game.save()

    # For each player, find all their matches, their scores in those
    # matches; then calculate their ratings. The new_ratings dictionary
    # contains players as keys, and dictionaries containing their new
    # rating parameters as the dictionary values.
    new_ratings = {}
    players = models.Player.objects.all()

    for player in players:
        # Don't calculate anything if the player's first game is prior
        # to this rating period
        # first_game_played = player.get_first_game_played()
        games_played_by_player = games.filter(Q(player1=player) | Q(player2=player))
        if games_played_by_player:
            print(f"{player} has played the following games:")
            for game in games_played_by_player:
                print(f"  - {game}")
        else:
            print(f"{player} has no games in the rating period")
        first_game_played = player.get_first_game_played()
        print(player)
        if (
                first_game_played is None
                or first_game_played.date_played > end_datetime
        ):
            continue

        # Get the players rating parameters
        player_rating = player.rating
        player_rating_deviation = player.rating_deviation
        player_inactivity = player.inactivity
        player_rating_volatility = player.rating_volatility

        opponent_ratings = []
        opponent_rating_deviations = []
        scores = []

        for game in games:
            if game.is_winner(player):
                scores.append(1.0)
            elif game.is_loser(player):
                scores.append(0.0)
            else:
                scores.append(0.5)

            if game.player1 == player:
                opponent_ratings.append(game.player2.rating)
                opponent_rating_deviations.append(game.player2.rating_deviation)
            elif game.player2 == player:
                opponent_ratings.append(game.player1.rating)
                opponent_rating_deviations.append(game.player1.rating_deviation)

        # Glicko-2
        new_player_rating, new_player_rating_deviation, new_player_rating_volatility = glicko2.calculate_player_rating(
            r=player_rating,
            RD=player_rating_deviation,
            sigma=player_rating_volatility,
            opponent_rs=opponent_ratings,
            opponent_RDs=opponent_rating_deviations,
            scores=scores,
        )

        # Calculate new inactivity
        new_player_inactivity = player_inactivity + 1 if not opponent_ratings else 0

        # Determine if the player is labeled as active
        new_player_is_active = new_player_inactivity < settings.NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE

        new_ratings[player] = {
            "player_ranking": None,
            "player_ranking_delta": None,
            "player_rating": new_player_rating,
            "player_rating_deviation": new_player_rating_deviation,
            "player_rating_volatility": new_player_rating_volatility,
            "player_inactivity": new_player_inactivity,
            "player_is_active": new_player_is_active,
        }

    # Filter all active players and sort by rating
    new_active_player_ratings = [
        (player, new_rating["player_rating"])
        for player, new_rating in new_ratings.items()
        if new_rating["player_is_active"]
    ]
    new_active_player_ratings.sort(key=lambda x: x[1], reverse=True)

    # Process new rankings and ranking changes
    num_active_players = len(new_active_player_ratings)

    # Keep track of the previous player's integer rating for ranking ties
    last_integer_rating = None
    last_ranking = None

    for idx, (player, rating) in enumerate(new_active_player_ratings, 1):
        integer_rating = round(rating)

        if (
                last_integer_rating is not None
                and last_integer_rating == integer_rating
        ):
            # Tie
            ranking = last_ranking
        else:
            last_integer_rating = integer_rating
            last_ranking = idx
            ranking = idx

        # Ranking
        new_ratings[player]["player_ranking"] = ranking

        # Ranking delta
        if player.ranking is None:
            new_ratings[player]["player_ranking_delta"] = (
                    num_active_players - ranking + 1
            )
        else:
            new_ratings[player]["player_ranking_delta"] = (
                    player.ranking - ranking
            )

    # Now save all ratings
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
