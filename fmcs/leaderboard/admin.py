from django.contrib import admin

from .models import Team, Event, Result, Organizator, Status


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_name', 'user', 'ranking']


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_name', 'org_name', 'status_name']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'team1', 'team2', 'result', 'match_date', 'event_id']


class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'org_name', 'description']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status_name']


admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Organizator, OrganizatorAdmin)
admin.site.register(Status, StatusAdmin)
