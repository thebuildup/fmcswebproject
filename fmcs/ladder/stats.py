"""Содержит функции для расчета статистики игроков и матчей.."""
# from .models import PlayerStatsNode, MatchupStatsNode


# from .models import PlayerStatsNode, MatchupStatsNode


from . import models


def calculate_new_average(avg, N, new_vals):
    print("calculate_new_average")
    """Рассчитать новое среднее значение с учетом нового значения и существующего среднего значения.
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
    """Рассчитать новую общую статистику для игрока.

    Это можно сделать в контексте всех игр или конкретной
    совпадают.

    Args:
        old_games: Количество игр, ранее сыгранных игроком.
        old_wins: Количество игр, выигранных игроком ранее.
        old_draws: Количество игр, разыгранных игроком ранее.
        old_losses: Количество игр, проигранных игроком ранее.
        old_average_goals_per_game: Предыдущее среднее количество голов за игру
            игрок забил.
        old_average_goals_against_per_game: Предыдущие средние цели
            за игру соперник(и) забили.
        player_is_winner: Буллево значение, указывающее, выиграл ли игрок
            игра.
        player_score: Количество голов, забитых игроком в рассматраиваемой игре.
        opponent_score: Количество голов, забитых соперником в рассматриваемой игре.

    Returns:
        Словарь, содержащий новое количество игр, побед, ничьих, поражений, 
        среднее количество голов за игру, среднее количество голов за игру и процент побед..
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
    print("new stats")
    new_stats['games'] = new_games
    new_stats['wins'] = new_wins
    new_stats['draws'] = new_draws
    new_stats['losses'] = new_losses
    new_stats['average_goals_per_game'] = new_average_goals_per_game
    new_stats['average_goals_against_per_game'] = new_average_goals_against_per_game
    new_stats['win_rate'] = new_win_rate

    return new_stats


def create_player_stats_node(player, game, previous_node=None):
    print("create_player_stats_node")
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

    # Накапливайте статистику с каждого матча игрока
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

    # Обновить статистику на основе накопленных значений
    player_stats_node.wins = wins
    player_stats_node.draws = draws
    player_stats_node.losses = losses

    if player_stats_node.games > 0:
        player_stats_node.average_goals_per_game = total_goals_scored / player_stats_node.games
        player_stats_node.average_goals_against_per_game = total_goals_conceded / player_stats_node.games

    # Рассчитайте и установите процент побед
    player_stats_node.win_rate = wins / player_stats_node.games if player_stats_node.games > 0 else 0.0

    player_stats_node.save()


def create_matchup_stats_node(player1, player2, game, previous_node=None):
    print("create_matchup_stats_node")

    # Получите предыдущую статистику (если она существует)
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
