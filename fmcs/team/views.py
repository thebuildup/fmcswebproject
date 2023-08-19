from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from glicko.models import Player, PlayerRatingNode, RatingPeriod, Match
from django.urls import reverse
from django.template.defaultfilters import slugify
import json


# Create your views here.
def team_profile(request, formatted_player_name):
    player = get_object_or_404(Player, formatted_name=formatted_player_name)

    player_ratings = PlayerRatingNode.objects.filter(player_id=player.id).order_by('-rating_period__end_datetime')

    ratings_data = [
        round(rating.rating) for rating in player_ratings
    ]

    reversed_ratings_data = list(reversed(ratings_data))

    rating_periods = RatingPeriod.objects.all().order_by('-end_datetime')[:len(reversed_ratings_data)]
    categories = [rp.end_datetime.strftime("%b") for rp in rating_periods]
    reversed_categories = list(reversed(categories))

    # Получение последних 5 матчей, где игрок может быть player1 или player2
    last_matches = Match.objects.filter(Q(player1=player) | Q(player2=player)).order_by('-date_played')[:5]

    win_rate = player.win_rate * 100

    context = {
        'player': player,
        'win_rate': win_rate,
        'series': json.dumps([
            {
                'name': 'Rating',
                'data': reversed_ratings_data,
            },
        ]),
        'categories': json.dumps(reversed_categories),
        'last_matches': last_matches,
    }

    return render(request, 'teams/team_profile.html', context)
