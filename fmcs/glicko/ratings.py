from django.utils import timezone
from .models import RatingPeriod, PlayerStatsNode, Match
from .glicko2 import calculate_player_rating


def calculate_new_rating_period(start_datetime, end_datetime):
    """Calculate a new ratings and a corresponding new rating period.

    Args:
        start_datetime: The datetime for the start of the rating period.
        end_datetime: The datetime for the end of the rating period.
    """
    # Step 1: Create the rating period
    new_rating_period = RatingPeriod.objects.create(start_datetime=start_datetime, end_datetime=end_datetime)

    # Step 2: Grab all games that will be in this rating period and mark them
    # as belonging to this rating period
    games_in_period = Match.objects.filter(date_played__range=(start_datetime, end_datetime))
    games_in_period.update(rating_period=new_rating_period)

    # Step 3: Calculate new ratings for each player
    players_with_games = PlayerStatsNode.objects.filter(games__gt=0).values_list('player', flat=True).distinct()

    new_ratings = {}
    for player_id in players_with_games:
        player_stats = PlayerStatsNode.objects.filter(player_id=player_id,
                                                      player__matches_as_player1__rating_period=new_rating_period)
        player_matches = player_stats.values_list('player__matches_as_player1', 'player1_goals', 'player2_goals')
        opponent_ratings = []
        opponent_RDs = []
        scores = []

        for match_id, player1_goals, player2_goals in player_matches:
            match = Match.objects.get(id=match_id)
            opponent_id = match.player2_id if player_id == match.player1_id else match.player1_id
            opponent_stats = PlayerStatsNode.objects.get(player_id=opponent_id,
                                                         player__matches_as_player1__rating_period=new_rating_period)

            opponent_ratings.append(opponent_stats.rating)
            opponent_RDs.append(opponent_stats.rating_deviation)

            if player1_goals > player2_goals:
                scores.append(1)  # Player won
            elif player1_goals < player2_goals:
                scores.append(0)  # Opponent won
            else:
                scores.append(0.5)  # Draw

        if len(opponent_ratings) == 0:
            # The player has no matches in this rating period, set opponent_ratings and opponent_RDs to None
            opponent_ratings = None
            opponent_RDs = None

        # Calculate the new rating, rating deviation, and rating volatility using Glicko-2
        new_rating, new_rating_deviation, new_rating_volatility = calculate_player_rating(
            r=player_stats.first().rating,
            RD=player_stats.first().rating_deviation,
            sigma=player_stats.first().rating_volatility,
            opponent_rs=opponent_ratings,
            opponent_RDs=opponent_RDs,
            scores=scores,
        )

        new_ratings[player_id] = {
            'rating': new_rating,
            'rating_deviation': new_rating_deviation,
            'rating_volatility': new_rating_volatility,
        }

    # Step 4: Update player stats nodes with the new ratings
    for player_id, new_params in new_ratings.items():
        player_stats_node = PlayerStatsNode.objects.get(player_id=player_id,
                                                        player__matches_as_player1__rating_period=new_rating_period)
        player_stats_node.rating = new_params['rating']
        player_stats_node.rating_deviation = new_params['rating_deviation']
        player_stats_node.rating_volatility = new_params['rating_volatility']
        player_stats_node.save()
