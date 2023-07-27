from django.contrib import admin

from .models import Player, PlayerStatsNode, PlayerRatingNode, RatingPeriod, Match, MatchupStatsNode


class ReadOnlyModelAdminMixin:
    """Mixin to make models read-only on admin page."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Register your models here.
@admin.register(RatingPeriod)
class RatingPeriodAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'ranking', 'rating', 'is_active')


@admin.register(PlayerStatsNode)
class PlayerStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('player', 'games', 'wins', 'draws', 'losses', 'win_rate', 'average_goals_per_game',
                    'average_goals_against_per_game')


@admin.register(PlayerRatingNode)
class PlayerRatingNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = (
        'player', 'rating_period', 'ranking', 'ranking_delta', 'rating', 'rating_deviation', 'rating_volatility',
        'inactivity', 'is_active')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ("rating_period",)
    list_max_show_all = 10000
    list_per_page = 200

    list_display = (
        'id', 'player1', 'player2', 'player1_goals', 'player2_goals', 'date_played', 'confirmed',
        'rating_period')


@admin.register(MatchupStatsNode)
class MatchupStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('player1', 'player2', 'game', 'games', 'wins', 'draws', 'losses',
                    'average_goals_per_game', 'average_goals_against_per_game', 'win_rate')
