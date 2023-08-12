from django.contrib import admin
from django.shortcuts import render
from import_export.admin import ImportExportModelAdmin
from .models import Player, PlayerStatsNode, PlayerRatingNode, RatingPeriod, Match, MatchupStatsNode
from .util import import_csv_to_match


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
# class PlayerAdmin(admin.ModelAdmin):
class PlayerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'user', 'ranking', 'rating', 'is_active')


@admin.register(PlayerStatsNode)
class PlayerStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('player', 'games', 'wins', 'draws', 'losses', 'win_rate', 'average_goals_per_game',
                    'average_goals_against_per_game')


@admin.register(PlayerRatingNode)
class PlayerRatingNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'player', 'rating_period', 'ranking', 'ranking_delta', 'rating', 'rating_deviation', 'rating_volatility',
        'inactivity', 'is_active')


@admin.register(Match)
# class MatchAdmin(admin.ModelAdmin):
class MatchAdmin(ImportExportModelAdmin):
    readonly_fields = ("rating_period",)
    list_max_show_all = 10000
    list_per_page = 200

    list_display = (
        'id', 'player1', 'player2', 'num_matches', 'player1_goals_m1', 'player2_goals_m1', 'player1_goals_m2',
        'player2_goals_m2',
        'player1_goals_m3', 'player2_goals_m3', 'player1_goals_m4', 'player2_goals_m4', 'player1_goals_m5',
        'player2_goals_m5', 'date_played', 'confirmed',
        'rating_period')
    actions = ['import_csv']

    def import_csv(self, request, queryset):
        if request.method == "POST" and "csv_file" in request.FILES:
            csv_file = request.FILES['csv_file']
            import_csv_to_match(csv_file)
            self.message_user(request, "CSV file has been imported successfully.")
        else:
            context = {"queryset": queryset}
            return render(request, "admin/import_csv.html", context)


@admin.register(MatchupStatsNode)
class MatchupStatsNodeAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('player1', 'player2', 'game', 'games', 'wins', 'draws', 'losses',
                    'average_goals_per_game', 'average_goals_against_per_game', 'win_rate')
