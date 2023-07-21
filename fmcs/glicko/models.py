from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


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
        """Returns the players ranking."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking

    @property
    def ranking_delta(self):
        """Returns the players ranking change."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return None

        return node.ranking_delta

    @property
    def rating(self):
        """Returns the players rating."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RATING

            return settings.GLICKO2_BASE_RATING

        return node.rating

    @property
    def rating_deviation(self):
        """Returns the players rating deviation."""
        node = self.get_latest_player_rating_node()

        if node is None:
            if settings.RATING_ALGORITHM == "glicko":
                return settings.GLICKO_BASE_RD

            return settings.GLICKO2_BASE_RD

        return node.rating_deviation

    @property
    def rating_volatility(self):
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
        """Returns the players rating period inactivity."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return 0

        return node.inactivity

    @property
    def is_active(self):
        """Returns whether the player is active."""
        node = self.get_latest_player_rating_node()

        if node is None:
            return False

        return node.is_active

    @property
    def games(self):
        """Returns the players game count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.games

    @property
    def wins(self):
        """Returns the players win count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.wins

    @property
    def draws(self):
        """Returns the players win count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.draws

    @property
    def losses(self):
        """Returns the players losses count."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.losses

    @property
    def win_rate(self):
        """Returns the players win rate."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.win_rate

    @property
    def average_goals_per_game(self):
        """Returns the players average goals per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_per_game

    @property
    def average_goals_against_per_game(self):
        """Returns the players average goals against per game."""
        node = self.get_latest_player_stats_node()

        if node is None:
            return 0

        return node.average_goals_against_per_game

    def get_all_player_stats_nodes(self):
        """Returns all of the player's stats nodes."""
        return PlayerStatsNode.objects.filter(player=self)

    def get_latest_player_stats_node(self):
        """Returns the player's latest stats node.

        Returns None if no stats nodes exist for the player.
        """
        nodes = self.get_all_player_stats_nodes()

        if nodes:
            return nodes.first()

        return None

    def get_all_matchup_stats_nodes(self, opponent):
        """Returns all of the player's matchup stats nodes against an opponent.

        Args:
            opponent: A Player model instance to filter against. If this
                isn't provided, matchup nodes will be returned for all
                opponents.
        """
        return MatchupStatsNode.objects.filter(player1=self, player2=opponent)

    def get_latest_matchup_stats_node(self, opponent):
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
        """Returns all of the player's rating nodes."""
        return PlayerRatingNode.objects.filter(player=self)

    def get_latest_player_rating_node(self):
        """Returns the player's latest rating node.

        Returns None if no rating nodes exist for the player.
        """
        nodes = self.get_all_player_rating_nodes()

        if nodes:
            return nodes.first()

        return None

    def get_first_game_played(self):
        """Returns the first game played by the player.

        Returns None if the player has not played games.
        """
        games_played = Match.objects.filter(Q(winner=self) | Q(loser=self))

        if not games_played:
            return None

        return games_played.last()


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
        help_text="The number of goals scored by the first player.",
    )
    player2_goals = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="The number of goals scored by the second player.",
    )

    player1_initial_rating = models.FloatField(
        default=1500.0,
        help_text="The initial rating of player1 before the match.",
    )

    player2_initial_rating = models.FloatField(
        default=1500.0,
        help_text="The initial rating of player2 before the match.",
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

    def process_game(self):
        """Process the match and update PlayerStatsNode and MatchupStatsNode."""
        for i in range(self.num_matches):
            # Обновить начальные рейтинги перед матчем
            player1_stats_node = PlayerStatsNode.objects.get_or_create(
                player=self.player1, defaults={
                    'games': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'average_goals_per_game': 0, 'average_goals_against_per_game': 0,
                    'rating': self.player1_initial_rating,
                    'rating_deviation': settings.GLICKO_BASE_RD,  # Или другое значение RD
                }
            )[0]

            player2_stats_node = PlayerStatsNode.objects.get_or_create(
                player=self.player2, defaults={
                    'games': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                    'average_goals_per_game': 0, 'average_goals_against_per_game': 0,
                    'rating': self.player2_initial_rating,
                    'rating_deviation': settings.GLICKO_BASE_RD,  # Или другое значение RD
                }
            )[0]

            # Обработать результаты матчей и обновить узлы статистики
            self.process_single_game(player1_stats_node, player2_stats_node)
            self.create_matchup_stats_node(player1_stats_node.player, player2_stats_node.player)

    def process_single_game(self, player1_stats_node, player2_stats_node):
        """Process a single game result and update PlayerStatsNode."""
        if self.player1_goals is not None and self.player2_goals is not None:
            # Обновить рейтинг игроков в зависимости от забитых голов
            # Например, используйте вашу реализацию расчета рейтинга на основе результатов матча

            # Обновить статистику игроков
            player1_stats_node.games += 1
            player2_stats_node.games += 1

            if self.player1_goals > self.player2_goals:
                player1_stats_node.wins += 1
                player2_stats_node.losses += 1
            elif self.player1_goals < self.player2_goals:
                player1_stats_node.losses += 1
                player2_stats_node.wins += 1
            else:
                player1_stats_node.draws += 1
                player2_stats_node.draws += 1

            player1_stats_node.average_goals_per_game = (
                                                                player1_stats_node.average_goals_per_game * (
                                                                player1_stats_node.games - 1) + self.player1_goals
                                                        ) / player1_stats_node.games
            player2_stats_node.average_goals_per_game = (
                                                                player2_stats_node.average_goals_per_game * (
                                                                player2_stats_node.games - 1) + self.player2_goals
                                                        ) / player2_stats_node.games

            player1_stats_node.average_goals_against_per_game = (
                                                                        player1_stats_node.average_goals_against_per_game * (
                                                                        player1_stats_node.games - 1) + self.player2_goals
                                                                ) / player1_stats_node.games
            player2_stats_node.average_goals_against_per_game = (
                                                                        player2_stats_node.average_goals_against_per_game * (
                                                                        player2_stats_node.games - 1) + self.player1_goals
                                                                ) / player2_stats_node.games

        player1_stats_node.save()
        player2_stats_node.save()

        # Добавьте дополнительные действия, если это нужно для обработки каждого сыгранного матча отдельно

    # Остальной код модели Match...


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
        return self.game.datetime_played


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


class MatchupStatsNode(models.Model):
    """Statistics of a matchup between two players."""
    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='matchups_as_player1',
        help_text="The first player in the matchup.",
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='matchups_as_player2',
        help_text="The second player in the matchup.",
    )
    games_played = models.PositiveIntegerField(
        default=0,
        help_text="The number of games played between the players in this matchup.",
    )
    player1_wins = models.PositiveIntegerField(
        default=0,
        help_text="The number of games won by the first player in this matchup.",
    )
    player2_wins = models.PositiveIntegerField(
        default=0,
        help_text="The number of games won by the second player in this matchup.",
    )
    draws = models.PositiveIntegerField(
        default=0,
        help_text="The number of draws in this matchup.",
    )
    losses = models.PositiveIntegerField(
        default=0,
        help_text="The number of games lost by both players in this matchup.",
    )
    average_goals_per_game_player1 = models.FloatField(
        default=0.0,
        help_text="The average number of goals scored by the first player in this matchup.",
    )
    average_goals_per_game_player2 = models.FloatField(
        default=0.0,
        help_text="The average number of goals scored by the second player in this matchup.",
    )
    win_percentage_player1 = models.FloatField(
        default=0.0,
        help_text="The percentage of wins for the first player in this matchup.",
    )
    win_percentage_player2 = models.FloatField(
        default=0.0,
        help_text="The percentage of wins for the second player in this matchup.",
    )
    draw_percentage = models.FloatField(
        default=0.0,
        help_text="The percentage of draws in this matchup.",
    )
    loss_percentage_player1 = models.FloatField(
        default=0.0,
        help_text="The percentage of losses for the first player in this matchup.",
    )
    loss_percentage_player2 = models.FloatField(
        default=0.0,
        help_text="The percentage of losses for the second player in this matchup.",
    )

    class Meta:
        """Model metadata."""
        unique_together = ('player1', 'player2')

    def __str__(self):
        """String representation of a matchup stats node."""
        return f"{self.player1.name} vs. {self.player2.name}"

    def update_stats(self):
        """Update matchup statistics based on the latest game results."""
        games = Match.objects.filter(player1=self.player1, player2=self.player2) | Match.objects.filter(
            player1=self.player2, player2=self.player1)
        self.games_played = games.count()
        self.player1_wins = games.filter(winner=self.player1).count()
        self.player2_wins = games.filter(winner=self.player2).count()
        self.draws = games.filter(winner=None).count()
        self.losses = games.exclude(winner=self.player1).exclude(winner=self.player2).count()

        player1_goals_sum = games.aggregate(models.Sum('player1_goals'))['player1_goals__sum']
        player2_goals_sum = games.aggregate(models.Sum('player2_goals'))['player2_goals__sum']

        if player1_goals_sum is not None and self.games_played > 0:
            self.average_goals_per_game_player1 = player1_goals_sum / self.games_played

        if player2_goals_sum is not None and self.games_played > 0:
            self.average_goals_per_game_player2 = player2_goals_sum / self.games_played

        if self.games_played > 0:
            self.win_percentage_player1 = (self.player1_wins / self.games_played) * 100
            self.win_percentage_player2 = (self.player2_wins / self.games_played) * 100
            self.draw_percentage = (self.draws / self.games_played) * 100
            self.loss_percentage_player1 = (self.losses / self.games_played) * 100
            self.loss_percentage_player2 = (self.losses / self.games_played) * 100

        self.save()


@receiver(post_save, sender=Match)
def process_game_hook(instance, created, **_):
    """Process a game immediately after game creation."""
    if created:
        instance.process_game()
