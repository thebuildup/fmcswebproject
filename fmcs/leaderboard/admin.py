from django.contrib import admin

from .models import (
    Team,
    Result,
    Game,
    MatchupStatsNode,
    Player,
    PlayerRatingNode,
    PlayerStatsNode,
    RatingPeriod
)


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_name', 'user', 'ranking']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'team1', 'team2', 'result', 'match_date', 'event_id']


class ReadOnlyModelAdminMixin:
    """Mixin to make models read-only on admin page."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RatingPeriod)
class RatingPeriodAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """Settings for RatingPeriod model on admin page."""

    list_display = ("id", "start_datetime", "end_datetime")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Settings for Game model on admin page."""

    readonly_fields = ("rating_period",)
    list_max_show_all = 10000
    list_per_page = 200

    list_display = (
        "id",
        "datetime_played",
        "winner",
        "loser",
        "winner_score",
        "loser_score",
        "event",
        "rating_period",
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Settings for Player model on admin page."""

    list_display = (
        "id",
        "name",
        "user",
        "is_active",
        "ranking",
        "ranking_delta",
        "rating",
        "rating_deviation",
        "rating_volatility",
        "inactivity",
        "games",
        "wins",
        "losses",
        "win_rate",
        "average_goals_per_game",
    )


@admin.register(PlayerStatsNode)
class PlayerStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """Settings for PlayerStatsNode model on admin page."""

    list_display = (
        "id",
        "player",
        "datetime",
        "games",
        "wins",
        "losses",
        "win_rate",
        "average_goals_per_game",
    )


@admin.register(PlayerRatingNode)
class PlayerRatingNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """Settings for PlayerRatingNode model on admin page."""

    list_display = (
        "id",
        "player",
        "ranking",
        "ranking_delta",
        "rating_period",
        "rating",
        "rating_deviation",
        "rating_volatility",
        "inactivity",
    )


@admin.register(MatchupStatsNode)
class MatchupStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """Settings for MatchupStatsNode model on admin page."""

    list_display = (
        "id",
        "player1",
        "player2",
        "datetime",
        "games",
        "wins",
        "losses",
        "win_rate",
        "average_goals_per_game",
    )


admin.site.register(Team, TeamAdmin)

admin.site.register(Result, ResultAdmin)
