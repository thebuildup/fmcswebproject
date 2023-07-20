from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


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
        games_played = Game.objects.filter(Q(winner=self) | Q(loser=self))

        if not games_played:
            return None

        return games_played.last()


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
        Game,
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
