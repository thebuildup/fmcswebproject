from django.contrib import admin

from .models import Tournament, Participant, Organizator


# Register your models here.
class ParticipantInline(admin.TabularInline):
    model = Participant


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'format', 'start_date', 'end_date', 'swiss_rounds')
    inlines = [ParticipantInline]


class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Participant)
admin.site.register(Organizator, OrganizatorAdmin)
