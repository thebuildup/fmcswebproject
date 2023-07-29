from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from . import stats


# Create your models here.
class RatingPeriod(models.Model):
    """A model for a Glicko rating period."""

    start_datetime = models.DateTimeField(
        help_text="The starting datetime for the rating period."
    )
    end_datetime = models.DateTimeField(
        help_text="The starting datetime for the rating period."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-end_datetime"]

    def __str__(self):
        """String representation of a rating period."""
        return str(self.id)


class Player(models.Model):
    """A model of a player and their stats."""

    name = models.CharField(
        max_length=200, unique=True, help_text="The player's name."
    )
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The user associated with the player.",
    )

    class Meta:
        """Model metadata."""

        # Order by name in ascending order
        ordering = ["name", "id"]

    def __str__(self):
        """String representation of a player."""
        return "%s #%04d" % (self.name, self.id)

    @property
    def ranking(self):
        print("ranking")
        """Returns the players ranking."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking

    @property
    def ranking_delta(self):
        print("ranking_delta")
        """Returns the players ranking change."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking_delta

    @property
    def rating(self):
        print("rating")
        """Returns the players rating."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RATING

            return settings.GLICKO2_BASE_RATING

        return node.rating

    @property
    def rating_deviation(self):
        print("rating_deviation")
        """Returns the players rating deviation."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RD

            return settings.GLICKO2_BASE_RD

        return node.rating_deviation

    @property
    def rating_volatility(self):
        print("rating_volatility")
        """Returns the players rating volatility.

        This parameter is only relevant if the rating algorithm is
        Glicko-2 and will always be None if the rating algorithm is
        Glicko (cf. Glicko-2).
        """
        # Get out if rating algorithm is Glicko
        if settings.RATING_ALGORITHM == "glicko":
            return None

        # Rating algorithm is Glicko-2
        node = self.get_latest_player_rating_node()

        if node is None:
            return settings.GLICKO2_BASE_VOLATILITY

        return node.rating_volatility

    @property
    def inactivity(self):
        print("inactivity")
        """Returns the players rating period inactivity."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return 0

        return node.inactivity

    @property
    def is_active(self):
        print("is_active")
        """Returns whether the player is active."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return False

        return node.is_active

    @property
    def games(self):
        print("games")
        """Returns the players game count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.games

    @property
    def wins(self):
        print("wins")
        """Returns the players win count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.wins

    @property
    def draws(self):
        print("draws")
        """Returns the players win count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.draws

    @property
    def losses(self):
        print("losses")
        """Returns the players losses count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.losses

    @property
    def win_rate(self):
        print("win_rate")
        """Returns the players win rate."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.win_rate

    @property
    def average_goals_per_game(self):
        print("average_goals_per_game")
        """Returns the players average goals per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_per_game

    @property
    def average_goals_against_per_game(self):
        print("average_goals_against_per_game")
        """Returns the players average goals against per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_against_per_game

    def get_all_player_stats_nodes(self):
        print("get_all_player_stats_nodes")
        """Returns all of the player's stats nodes."""
        return PlayerStatsNode.objects.filter(player=self)

    def get_latest_player_stats_node(self):
        print("get_latest_player_stats_node")
        """Returns the player's latest stats node.

        Returns None if no stats nodes exist for the player.
        """
        nodes = self.get_all_player_stats_nodes()

        if nodes:
            return nodes.first()

        return None

    def get_all_matchup_stats_nodes(self, opponent):
        print("get_all_matchup_stats_nodes")
        """Returns all of the player's matchup stats nodes against an opponent.

        Args:
            opponent: A Player model instance to filter against. If this
                isn't provided, matchup nodes will be returned for all
                opponents.
        """
        return MatchupStatsNode.objects.filter(player1=self, player2=opponent)

    def get_latest_matchup_stats_node(self, opponent):
        print("get_latest_matchup_stats_node")
        print(opponent)
        """Returns the player's latest matchup stats node against an opponent.

        Args:
            opponent: A Player model instance to filter against. If this
                isn't provided, matchup nodes will be returned for all
                opponents.
        """
        nodes = self.get_all_matchup_stats_nodes(opponent)

        if nodes:
            return nodes.first()

        return None

    def get_all_player_rating_nodes(self):
        print("get_all_player_rating_nodes")
        """Returns all of the player's rating nodes."""
        return PlayerRatingNode.objects.filter(player=self)

    def get_latest_player_rating_node(self):
        print("get_latest_player_rating_node")
        """Returns the player's latest rating node.

        Returns None if no rating nodes exist for the player.
        """
        nodes = self.get_all_player_rating_nodes()

        if nodes:
            return nodes.first()

        return None

    # def get_first_game_played(self):
    #     print("get_first_game_played")
    #     """Returns the first game played by the player.
    #
    #     Returns None if the player has not played games.
    #     """
    #     games_played = Match.objects.filter(Q(winner=self) | Q(loser=self))
    #
    #     if not games_played:
    #         return None
    #
    #     return games_played.last()

    def get_first_game_played(self):
        games_played = Match.objects.filter(
            Q(player1=self) | Q(player2=self)
        ).order_by('date_played')

        if not games_played:
            return None

        return games_played.first()


class Match(models.Model):
    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='matches_as_player1',
        help_text="The first player in the match.",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='matches_as_player2',
        help_text="The second player in the match.",
    )

    num_matches = models.PositiveSmallIntegerField(
        default=1,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        help_text="The number of matches played between the players (1 to 5)."
    )

    player1_goals = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the first player in first match.",
    )
    player2_goals = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player in first match.",
    )
    player1_goals_m2 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the first player in second match.",
    )
    player2_goals_m2 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player in second match.",
    )
    player1_goals_m3 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the first player in third match.",
    )
    player2_goals_m3 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player in third match.",
    )
    player1_goals_m4 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the first player in fourth match.",
    )
    player2_goals_m4 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player in fourth match.",
    )
    player1_goals_m5 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the first player in fifth match.",
    )
    player2_goals_m5 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player in fifth match.",
    )

    date_played = models.DateTimeField(
        # auto_now_add=True,
        default=timezone.now,
        help_text="The date and time when the game was played.",
    )
    confirmed = models.ForeignKey(
        User,
        default=False,
        on_delete=models.PROTECT,
        help_text="The user which submitted the game.",
    )
    rating_period = models.ForeignKey(
        RatingPeriod,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The rating period this game is apart of",
    )

    class Meta:
        """Model metadata."""

        # Order by most recently played
        ordering = ["-date_played"]

    def __str__(self):
        """String representation of a game."""
        return str(self.id)

    @property
    def player1_player_stats_node(self):
        print("player1_player_stats_node")
        """Return the player stats node for the winner."""
        node_queryset = self.playerstatsnode_set.filter(
            player=self.player1, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def player2_player_stats_node(self):
        print("player2_player_stats_node")
        """Return the player stats node for the loser."""
        node_queryset = self.playerstatsnode_set.filter(
            player=self.player2, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def player1_matchup_stats_node(self):
        print("player1_matchup_stats_node")
        """Return the matchup stats node for the winner."""
        node_queryset = self.matchupstatsnode_set.filter(
            player1=self.player1, player2=self.player2, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    @property
    def player2_matchup_stats_node(self):
        print("player2_matchup_stats_node")
        """Return the matchup stats node for the loser."""
        node_queryset = self.matchupstatsnode_set.filter(
            player2=self.player1, player1=self.player2, game=self
        )

        if node_queryset:
            return node_queryset.first().id

        return None

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError("Player 1 and Player 2 must be distinct!")

    def process_game(self):
        print("process_game")
        """Process the match and update PlayerStatsNode and MatchupStatsNode."""
        num_matches = self.num_matches

        if self.player1_player_stats_node is None:
            stats.create_player_stats_node(
                player=self.player1,
                game=self,
                previous_node=self.player1.get_latest_player_stats_node(),
            )

        if self.player2_player_stats_node is None:
            stats.create_player_stats_node(
                player=self.player2,
                game=self,
                previous_node=self.player2.get_latest_player_stats_node(),
            )

        if self.player1_matchup_stats_node is None:
            stats.create_matchup_stats_node(
                player1=self.player1,
                player2=self.player2,
                game=self,
                previous_node=self.player1.get_latest_matchup_stats_node(
                    self.player2
                ),
            )

        if self.player2_matchup_stats_node is None:
            stats.create_matchup_stats_node(
                player1=self.player2,
                player2=self.player1,
                game=self,
                previous_node=self.player2.get_latest_matchup_stats_node(
                    self.player1
                ),
            )

    def is_winner(self, player):
        """Проверяет, является ли данный игрок победителем матча на основе забитых голов.

        Аргументы:
            player: Экземпляр модели Player для проверки.

        Возвращает:
            True, если данный игрок является победителем, иначе False.
        """
        if (player == self.player1 and self.player1_goals > self.player2_goals) or \
                (player == self.player2 and self.player2_goals > self.player1_goals):
            return True
        else:
            return False

    def is_loser(self, player):
        """Проверяет, является ли данный игрок проигравшим матча на основе забитых голов.

        Аргументы:
            player: Экземпляр модели Player для проверки.

        Возвращает:
            True, если данный игрок является проигравшим, иначе False.
        """
        if (player == self.player1 and self.player1_goals < self.player2_goals) or \
                (player == self.player2 and self.player2_goals < self.player1_goals):
            return True
        else:
            return False

    def is_draw(self, player):
        """Проверяет, является ли данный игрок участником ничьей в матче на основе забитых голов.

        Аргументы:
            player: Экземпляр модели Player для проверки.

        Возвращает:
            True, если данный игрок участвовал в ничьей, иначе False.
        """
        if (player == self.player1 or player == self.player2) and self.player1_goals == self.player2_goals:
            return True
        else:
            return False

    def get_player_goals(self, player):
        print("get_player_goals")
        """Возвращает количество забитых голов указанного игрока в матче.

        Аргументы:
            player: Экземпляр модели Player для получения забитых голов.

        Возвращает:
            Количество забитых голов указанного игрока в текущем матче.
        """
        if player == self.player1:
            return self.player1_goals
        elif player == self.player2:
            return self.player2_goals
        else:
            raise ValueError("Player is not a participant in this match.")

    def get_opponent_goals(self, player):
        print("get_player_goals")
        """Возвращает количество забитых голов указанного игрока в матче.

        Аргументы:
            player: Экземпляр модели Player для получения забитых голов.

        Возвращает:
            Количество забитых голов указанного игрока в текущем матче.
        """
        if player == self.player1:
            return self.player2_goals
        elif player == self.player2:
            return self.player1_goals
        else:
            raise ValueError("Player is not a participant in this match.")

    # def get_player_initial_rating(self, player):
    #     print("get_player_initial_rating")
    #     """Get the initial rating of the player from PlayerRankingNode."""
    #     try:
    #         player_ranking_node = PlayerRatingNode.objects.get(player=player)
    #         return player_ranking_node.rating
    #     except PlayerRatingNode.DoesNotExist:
    #         return settings.GLICKO_BASE_RATING  # Если узел не найден, используйте значение по умолчанию

    def process_single_game(self, player1_stats_node, player2_stats_node, player1_goals, player2_goals):
        print("process_single_game")
        """Process a single game result and update PlayerStatsNode."""
        if player1_goals is not None and player2_goals is not None:
            # Обновить статистику игроков
            player1_stats_node.games += 1
            player2_stats_node.games += 1

            if player1_goals > player2_goals:
                player1_stats_node.wins += 1
                player2_stats_node.losses += 1
            elif player1_goals < player2_goals:
                player1_stats_node.losses += 1
                player2_stats_node.wins += 1
            else:
                player1_stats_node.draws += 1
                player2_stats_node.draws += 1

            # Используем функцию для пересчета средних значений
            player1_stats_node.average_goals_per_game = stats.calculate_new_average(
                player1_stats_node.average_goals_per_game, player1_stats_node.games - 1, player1_goals
            )
            player2_stats_node.average_goals_per_game = stats.calculate_new_average(
                player2_stats_node.average_goals_per_game, player2_stats_node.games - 1, player2_goals
            )

            player1_stats_node.average_goals_against_per_game = stats.calculate_new_average(
                player1_stats_node.average_goals_against_per_game, player1_stats_node.games - 1, player2_goals
            )
            player2_stats_node.average_goals_against_per_game = stats.calculate_new_average(
                player2_stats_node.average_goals_against_per_game, player2_stats_node.games - 1, player1_goals
            )

        player1_stats_node.save()
        player2_stats_node.save()


class PlayerStatsNode(models.Model):
    """A player's stats snapshot at a particular point in time

    A node will be generated for each game played by a player.
    """

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        help_text="The player to record stats for.",
    )
    game = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        help_text="The game which updated the player's stats.",
    )
    games = models.PositiveIntegerField(
        help_text="The number of games a player has played."
    )
    wins = models.PositiveIntegerField(
        help_text="The number of wins the player has."
    )
    draws = models.PositiveIntegerField(
        help_text="The number of draws the player has."
    )
    losses = models.PositiveIntegerField(
        help_text="The number of losses the player has."
    )
    win_rate = models.FloatField(
        null=True,
        help_text="The player's win rate."
    )
    average_goals_per_game = models.FloatField(
        help_text="The average number of goals scored per game by the player."
    )
    average_goals_against_per_game = models.FloatField(
        help_text="The average number of goals scored against the player per game."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a player stats node."""
        return "%s (game ID: %s; date: %s)" % (
            self.player,
            self.game.id,
            self.datetime,
        )

    @property
    def datetime(self):
        """Returns the date of the node's game."""
        return self.game.date_played


class PlayerRatingNode(models.Model):
    """A player's rating for a given rating period."""

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        help_text="The player corresponding whose ratings this node is for.",
    )
    rating_period = models.ForeignKey(
        RatingPeriod,
        on_delete=models.CASCADE,
        help_text="The rating period this rating was calculated in.",
    )
    ranking = models.PositiveSmallIntegerField(
        null=True, help_text="The player's rating for this rating period."
    )
    ranking_delta = models.SmallIntegerField(
        null=True,
        help_text="The player's rating change for this rating period.",
    )
    rating = models.FloatField(
        help_text="The player's rating for this rating period."
    )
    rating_deviation = models.FloatField(
        help_text="The player's rating deviation for this rating period."
    )
    rating_volatility = models.FloatField(
        null=True,
        help_text="The player's rating volatility for this rating period. This is only used if the rating algorithm is Glicko-2.",
    )
    inactivity = models.PositiveSmallIntegerField(
        help_text="How many rating periods the player has been inactive for."
    )
    is_active = models.BooleanField(
        help_text="Whether the player was considered active during this rating period."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a player rating node.

        Only shows rating volatility if the rating algorithm is
        Glicko-2.
        """
        if settings.RATING_ALGORITHM == "glicko":
            return "%s RP=%s r=%d, RD=%d" % (
                self.player,
                self.rating_period.id,
                self.rating,
                self.rating_deviation,
            )

        return "%s RP=%s r=%d, RD=%d, σ=%.2f" % (
            self.player,
            self.rating_period.id,
            self.rating,
            self.rating_deviation,
            self.rating_volatility,
        )


# class MatchupStatsNode(models.Model):
#     """Statistics of a matchup between two players."""
#     player1 = models.ForeignKey(
#         Player,
#         on_delete=models.CASCADE,
#         related_name='matchups_as_player1',
#         help_text="The first player in the matchup.",
#     )
#     player2 = models.ForeignKey(
#         Player,
#         on_delete=models.CASCADE,
#         related_name='matchups_as_player2',
#         help_text="The second player in the matchup.",
#     )
#     games_played = models.PositiveIntegerField(
#         default=0,
#         help_text="The number of games played between the players in this matchup.",
#     )
#     player1_wins = models.PositiveIntegerField(
#         default=0,
#         help_text="The number of games won by the first player in this matchup.",
#     )
#     player2_wins = models.PositiveIntegerField(
#         default=0,
#         help_text="The number of games won by the second player in this matchup.",
#     )
#     draws = models.PositiveIntegerField(
#         default=0,
#         help_text="The number of draws in this matchup.",
#     )
#     losses = models.PositiveIntegerField(
#         default=0,
#         help_text="The number of games lost by both players in this matchup.",
#     )
#     average_goals_per_game_player1 = models.FloatField(
#         default=0.0,
#         help_text="The average number of goals scored by the first player in this matchup.",
#     )
#     average_goals_per_game_player2 = models.FloatField(
#         default=0.0,
#         help_text="The average number of goals scored by the second player in this matchup.",
#     )
#     win_percentage_player1 = models.FloatField(
#         default=0.0,
#         help_text="The percentage of wins for the first player in this matchup.",
#     )
#     win_percentage_player2 = models.FloatField(
#         default=0.0,
#         help_text="The percentage of wins for the second player in this matchup.",
#     )
#     draw_percentage = models.FloatField(
#         default=0.0,
#         help_text="The percentage of draws in this matchup.",
#     )
#     loss_percentage_player1 = models.FloatField(
#         default=0.0,
#         help_text="The percentage of losses for the first player in this matchup.",
#     )
#     loss_percentage_player2 = models.FloatField(
#         default=0.0,
#         help_text="The percentage of losses for the second player in this matchup.",
#     )
#
#     class Meta:
#         """Model metadata."""
#         unique_together = ('player1', 'player2')
#
#     def __str__(self):
#         """String representation of a matchup stats node."""
#         return f"{self.player1.name} vs. {self.player2.name}"
#
#     def update_stats(self):
#         """Update matchup statistics based on the latest game results."""
#         games = Match.objects.filter(player1=self.player1, player2=self.player2) | Match.objects.filter(
#             player1=self.player2, player2=self.player1)
#         self.games_played = games.count()
#         self.player1_wins = games.filter(winner=self.player1).count()
#         self.player2_wins = games.filter(winner=self.player2).count()
#         self.draws = games.filter(winner=None).count()
#         self.losses = games.exclude(winner=self.player1).exclude(winner=self.player2).count()
#
#         player1_goals_sum = games.aggregate(models.Sum('player1_goals'))['player1_goals__sum']
#         player2_goals_sum = games.aggregate(models.Sum('player2_goals'))['player2_goals__sum']
#
#         if player1_goals_sum is not None and self.games_played > 0:
#             self.average_goals_per_game_player1 = player1_goals_sum / self.games_played
#
#         if player2_goals_sum is not None and self.games_played > 0:
#             self.average_goals_per_game_player2 = player2_goals_sum / self.games_played
#
#         if self.games_played > 0:
#             self.win_percentage_player1 = (self.player1_wins / self.games_played) * 100
#             self.win_percentage_player2 = (self.player2_wins / self.games_played) * 100
#             self.draw_percentage = (self.draws / self.games_played) * 100
#             self.loss_percentage_player1 = (self.losses / self.games_played) * 100
#             self.loss_percentage_player2 = (self.losses / self.games_played) * 100
#
#         self.save()
class MatchupStatsNode(models.Model):
    """A player matchup's stats snapshot at a particular point in time

    Two matchup nodes will be generated for each game played by a given
    matchup, each from the perspective of one of the players.
    """

    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player1",
        help_text="The player in the matchup whose perspective to take.",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player2",
        help_text='The "opponent" player in the matchup.',
    )
    game = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        help_text="The game which updated the matchup's stats.",
    )
    games = models.PositiveIntegerField(
        help_text="The number of games played by the matchup."
    )
    wins = models.PositiveIntegerField(
        help_text="The number of wins the player1 has."
    )
    draws = models.PositiveIntegerField(
        help_text="The number of draws the player1 has."
    )
    losses = models.PositiveIntegerField(
        help_text="The number of losses the player1 has."
    )
    win_rate = models.FloatField(
        help_text="player1's win rate against player2."
    )
    average_goals_per_game = models.FloatField(
        help_text="The average number of goals scored per game by player1."
    )
    average_goals_against_per_game = models.FloatField(
        help_text="The average number of goals scored per game by player2."
    )

    class Meta:
        """Model metadata."""

        # Order by creation date (in order from most recent to oldest)
        ordering = ["-id"]

    def __str__(self):
        """String representation of a matchup stats node."""
        return "%s vs %s (game ID: %s; date: %s)" % (
            self.player1,
            self.player2,
            self.game.id,
            self.datetime,
        )

    @property
    def datetime(self):
        """Returns the date of the node's game."""
        return self.game.date_played


@receiver(post_save, sender=Match)
def process_game_hook(instance, created, **_):
    print("process_game_hook")
    """Process a game immediately after game creation."""
    if created:
        instance.process_game()
