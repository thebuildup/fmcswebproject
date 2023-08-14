from django.shortcuts import render
from glicko.models import Player
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your views here.
def team_profile(request, player_id):
    player = Player.objects.get(pk=player_id)

    # Create a player link in the format: playername-id
    # player_link = f"{slugify(player.name)}-{player.id}"

    context = {
        'player': player,
    }

    return render(request, 'teams/team_profile.html', context)
