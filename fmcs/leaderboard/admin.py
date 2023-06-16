from django.contrib import admin
from .models import Team, Event, Result


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_name', 'user', 'ranking']


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'team1', 'team2', 'result', 'match_date', 'event_id']


admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
