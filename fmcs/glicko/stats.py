"""Contains functions for calculating player and matchup statistics."""
# from .models import PlayerStatsNode, MatchupStatsNode


# from .models import PlayerStatsNode, MatchupStatsNode


from . import models


# def calculate_new_average(avg, N, new_val):
def calculate_new_average(avg, N, new_vals):
    print("calculate_new_average")
    """Calculate new average given a new value and an existing average.

    Args:
        avg: The old average value.
        N: The old number of data points averaged over.
        new_val: The new value to recalculate the average with.

    Returns:
        The new average value.
    """
    if isinstance(new_vals, list):
        return (avg * N + sum(new_vals)) / (N + len(new_vals))
    else:
        return (avg * N + new_vals) / (N + 1)


def calculate_new_common_stats(old_games, old_wins, old_draws, old_losses,
                               old_average_goals_per_game, old_average_goals_against_per_game,
                               player_is_winner, player_score, opponent_score):
    print("calculate_new_common_stats")
    print(player_is_winner)
    """Calculate new common stats for a player.

    This can be done in the context of all games or a particular
    matchup.

    Args:
        old_games: The number of games previously played by the player.
        old_wins: The number of games won previously by the player.
        old_draws: The number of games draw previously by the player.
        old_losses: The number of games lost previously by the player.
        old_average_goals_per_game: The previous average goals per game
            the player scored.
        old_average_goals_against_per_game: The previous average goals
            per game the opponent(s) scored.
        player_is_winner: A boolean indicating whether the player won
            the game.
        player_score: The number of goals the player scored for the game
            under consideration.
        opponent_score: The number of goals the opponent scored for the
            game under consideration.

    Returns:
        A dictionary containing the new number of games, wins, draws, losses,
        average goals per game, average goals against per game, and win
        rate.
    """
    new_stats = {}
    new_games = old_games + 1
    new_wins = old_wins + int(player_is_winner)
    new_draws = old_draws + int(not player_is_winner and player_score == opponent_score)
    new_losses = old_losses + int(not player_is_winner and player_score < opponent_score)

    new_average_goals_per_game = calculate_new_average(
        old_average_goals_per_game, old_games, player_score
    )
    new_average_goals_against_per_game = calculate_new_average(
        old_average_goals_against_per_game, old_games, opponent_score
    )

    new_win_rate = new_wins / new_games
    # new_draw_rate = new_draws / new_games
    # new_lose_rate = new_losses / new_games
    print("new stats")
    new_stats['games'] = new_games
    new_stats['wins'] = new_wins
    new_stats['draws'] = new_draws
    new_stats['losses'] = new_losses
    new_stats['average_goals_per_game'] = new_average_goals_per_game
    new_stats['average_goals_against_per_game'] = new_average_goals_against_per_game
    new_stats['win_rate'] = new_win_rate
    # new_stats['draw_rate'] = new_draw_rate
    # new_stats['lose_rate'] = new_lose_rate

    return new_stats


# def create_player_stats_node(player, game, previous_node=None):
#     print("create_player_stats_node")
#     """Create a stats node for a player.
#
#     Args:
#         player: An instance of the Player model corresponding to the
#             player.
#         game: An instance of the Match model corresponding to the game to
#             adjust stats from.
#         previous_node: An optional instance of the PlayerStatsNode model
#             corresponding to the player's last stats node.
#     """
#     player_stats_node = models.PlayerStatsNode()
#
#     player_stats_node.player = player
#     player_stats_node.game = game
#
#     # Set initial values if previous_node is not provided
#     if previous_node is None:
#         player_stats_node.games = 1
#         player_stats_node.wins = 1 if game.is_winner(player) else 0
#         player_stats_node.draws = 1 if game.is_draw(player) else 0
#         player_stats_node.losses = 1 if game.is_loser(player) else 0
#         player_stats_node.average_goals_per_game = game.get_player_goals(player)
#         player_stats_node.average_goals_against_per_game = game.get_opponent_goals(player)
#         # player_stats_node.rating = player.initial_rating
#         # player_stats_node.rating_deviation = player.initial_rd
#
#     # Set values based on previous_node if provided
#     else:
#         player_stats_node.games = previous_node.games + 1
#         player_stats_node.wins = previous_node.wins + int(game.is_winner(player))
#         player_stats_node.draws = previous_node.draws + int(game.is_draw(player))
#         player_stats_node.losses = previous_node.losses + int(game.is_loser(player))
#         player_stats_node.average_goals_per_game = calculate_new_average(
#             previous_node.average_goals_per_game, previous_node.games, game.get_player_goals(player)
#         )
#         player_stats_node.average_goals_against_per_game = calculate_new_average(
#             previous_node.average_goals_against_per_game, previous_node.games, game.get_opponent_goals(player)
#         )
#         # player_stats_node.rating = previous_node.rating
#         # player_stats_node.rating_deviation = previous_node.rating_deviation
#
#     # Calculate and set the win rate, draw rate, and lose rate
#     player_stats_node.win_rate = player_stats_node.wins / player_stats_node.games
#     # player_stats_node.draw_rate = player_stats_node.draws / player_stats_node.games
#     # player_stats_node.lose_rate = player_stats_node.losses / player_stats_node.games
#
#     player_stats_node.save()

def create_player_stats_node(player, game, previous_node=None):
    print("create_player_stats_node")
    """Create a stats node for a player.

    Args:
        player: An instance of the Player model corresponding to the player.
        game: An instance of the Match model corresponding to the game to adjust stats from.
        previous_node: An optional instance of the PlayerStatsNode model corresponding to the player's last stats node.
    """
    player_stats_node = models.PlayerStatsNode()
    player_stats_node.player = player
    player_stats_node.game = game

    if previous_node is None:
        player_stats_node.games = 0
        player_stats_node.wins = 0
        player_stats_node.draws = 0
        player_stats_node.losses = 0
        player_stats_node.average_goals_per_game = 0.0
        player_stats_node.average_goals_against_per_game = 0.0
    else:
        player_stats_node.games = previous_node.games
        player_stats_node.wins = previous_node.wins
        player_stats_node.draws = previous_node.draws
        player_stats_node.losses = previous_node.losses
        player_stats_node.average_goals_per_game = previous_node.average_goals_per_game
        player_stats_node.average_goals_against_per_game = previous_node.average_goals_against_per_game

    # Accumulate stats from each match of the player
    wins = player_stats_node.wins
    draws = player_stats_node.draws
    losses = player_stats_node.losses
    total_goals_scored = player_stats_node.average_goals_per_game * player_stats_node.games
    total_goals_conceded = player_stats_node.average_goals_against_per_game * player_stats_node.games

    for i in range(game.num_matches):
        player1_goals = getattr(game, f'player1_goals_m{i + 1}', None)
        player2_goals = getattr(game, f'player2_goals_m{i + 1}', None)

        if player1_goals is not None and player2_goals is not None:
            player_stats_node.games += 1

            if player1_goals > player2_goals:
                wins += 1
            elif player1_goals < player2_goals:
                losses += 1
            else:
                draws += 1

            total_goals_scored += player1_goals
            total_goals_conceded += player2_goals

    # Update stats based on the accumulated values
    player_stats_node.wins = wins
    player_stats_node.draws = draws
    player_stats_node.losses = losses

    if player_stats_node.games > 0:
        player_stats_node.average_goals_per_game = total_goals_scored / player_stats_node.games
        player_stats_node.average_goals_against_per_game = total_goals_conceded / player_stats_node.games

    # Calculate and set the win rate, draw rate, and lose rate
    player_stats_node.win_rate = wins / player_stats_node.games if player_stats_node.games > 0 else 0.0
    # player_stats_node.draw_rate = draws / player_stats_node.games if player_stats_node.games > 0 else 0.0
    # player_stats_node.lose_rate = losses / player_stats_node.games if player_stats_node.games > 0 else 0.0

    player_stats_node.save()


def create_matchup_stats_node(player1, player2, game, previous_node=None):
    print("create_matchup_stats_node")

    """Create a stats node for a player.

    Args:
        player1: An instance of the Player model corresponding to the
            player whose perspective to take.
        player2: An instance of the Player model corresponding to the
            opponent player.
        game: An instance of the Match model corresponding to the game to
            adjust stats from.
        previous_node: An optional instance of the MatchupStatsNode
            model corresponding to the matchup's last stats node
            (between player 1 and 2—in that order—as provided).
    """

    # Grab previous stats (if they exist)
    if previous_node is not None:
        games = previous_node.games
        wins = previous_node.wins
        draws = previous_node.draws
        losses = previous_node.losses
        average_goals_per_game = previous_node.average_goals_per_game
        average_goals_against_per_game = (
            previous_node.average_goals_against_per_game
        )
    else:
        games = 0
        wins = 0
        draws = 0
        losses = 0
        average_goals_per_game = 0.0
        average_goals_against_per_game = 0.0

    # player_score = []
    # opponent_score = []

    total_goals_scored = average_goals_per_game * games
    total_goals_conceded = average_goals_against_per_game * games

    for i in range(1, game.num_matches + 1):
        player1_goals = getattr(game, f'player1_goals_m{i}', None)
        player2_goals = getattr(game, f'player2_goals_m{i}', None)

        if player1_goals is not None and player2_goals is not None:
            games += 1

            if player1_goals > player2_goals:
                wins += 1
            elif player1_goals < player2_goals:
                losses += 1
            else:
                draws += 1

            total_goals_scored += player1_goals
            total_goals_conceded += player2_goals

    win_rate = wins / games if games > 0 else 0.0

    if games > 0:
        average_goals_per_game = total_goals_scored / games
        average_goals_against_per_game = total_goals_conceded / games

    models.MatchupStatsNode.objects.create(
        player1=player1,
        player2=player2,
        game=game,
        games=games,
        wins=wins,
        draws=draws,
        losses=losses,
        average_goals_per_game=average_goals_per_game,
        average_goals_against_per_game=average_goals_against_per_game,
        win_rate=win_rate,
    )
