"""Contains serializers for models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from .models import (
    Match,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod,
)


class RatingPeriodSerializer(serializers.ModelSerializer):
    """A serializer for a rating period.

    This should be read-only.
    """

    class Meta:
        model = RatingPeriod
        fields = ("id", "start_datetime", "end_datetime")


class PlayerSerializer(serializers.ModelSerializer):
    """A serializer for a player."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Player

        fields = (
            "id",
            "name",
            "user",
            "country",
            "is_active",
            "ranking",
            "ranking_delta",
            "rating",
            "rating_deviation",
            "inactivity",
            "games",
            "wins",
            "draws",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )
        read_only_fields = (
            "id",
            "is_active",
            "ranking",
            "ranking_delta",
            "rating",
            "rating_deviation",
            "inactivity",
            "games",
            "wins",
            "draws",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )

        # Only show rating volatility if rating algorithm is Glicko-2
        if settings.RATING_ALGORITHM == "glicko2":
            fields = fields[:8] + ("rating_volatility",) + fields[8:]
            read_only_fields = (
                    fields[:6] + ("rating_volatility",) + read_only_fields[6:]
            )


class PlayerStatsNodeSerializer(serializers.ModelSerializer):
    """A serializer for a player stats node.

    This is meant to be read-only (stats nodes are handled exclusively
    by the backend).
    """

    # Need to specify this manually here since datetime is a property
    # and hence the default timezone settings don't automatically apply
    # to this
    datetime = serializers.DateTimeField(
        default=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
        initial=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
    )

    class Meta:
        model = PlayerStatsNode
        fields = (
            "id",
            "datetime",
            "player",
            "game",
            "games",
            "wins",
            "draws",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )


class MatchupStatsNodeSerializer(serializers.ModelSerializer):
    """A serializer for a matchup stats node.

    This is meant to be read-only (stats nodes are handled exclusively
    by the backend).
    """

    # Need to specify this manually here since datetime is a property
    # and hence the default timezone settings don't automatically apply
    # to this
    datetime = serializers.DateTimeField(
        default=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
        initial=lambda: timezone.localtime().strftime(
            settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        ),
    )

    class Meta:
        model = MatchupStatsNode
        fields = (
            "id",
            "datetime",
            "player1",
            "player2",
            "game",
            "games",
            "wins",
            "losses",
            "win_rate",
            "average_goals_per_game",
            "average_goals_against_per_game",
        )


class PlayerNameSerializer(serializers.ModelSerializer):
    """A serializer for a player."""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Player

        fields = (
            "id",
            "name",
            "user",
        )
        read_only_fields = (
            "id",
        )


class PlayerRatingNodeSerializer(serializers.ModelSerializer):
    """A serializer for a player rating node.

    This is meant to be read-only.
    """
    player = PlayerNameSerializer()

    class Meta:
        model = PlayerRatingNode

        fields = (
            "id",
            "player",
            "rating_period",
            "ranking",
            "ranking_delta",
            "rating",
            "rating_deviation",
            "inactivity",
        )

        # Only show rating volatility if rating algorithm is Glicko-2
        if settings.RATING_ALGORITHM == "glicko2":
            fields = fields[:7] + ("rating_volatility",) + fields[7:]

# class MatchSerializer(serializers.ModelSerializer):
#     """A serializer for a game.
#
#     Note that the user is automatically injected into the submitted_by
#     field for post methods.
#     """
#
#     winner_score = serializers.IntegerField(min_value=0, initial=8)
#     loser_score = serializers.IntegerField(min_value=0, initial=0)
#     submitted_by = serializers.SlugRelatedField(
#         queryset=User.objects.all(), slug_field="username"
#     )
#
#     class Meta:
#         model = Match
#         fields = (
#             "id",
#             "datetime_played",
#             "winner",
#             "loser",
#             "winner_score",
#             "loser_score",
#             "submitted_by",
#             "rating_period",
#             "winner_player_stats_node",
#             "loser_player_stats_node",
#             "winner_matchup_stats_node",
#             "loser_matchup_stats_node",
#         )
#         read_only_fields = (
#             "id",
#             "datetime_played",
#             "rating_period",
#             "winner_player_stats_node",
#             "loser_player_stats_node",
#             "winner_matchup_stats_node",
#             "loser_matchup_stats_node",
#         )
#
#     def validate(self, attrs):
#         """Call model's clean method."""
#         attrs = super().validate(attrs)
#
#         try:
#             Match(**attrs).clean()
#         except ValidationError as e:
#             raise serializers.ValidationError(str(e))
#
#         return attrs
