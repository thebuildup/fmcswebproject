from django.shortcuts import render
from glicko.models import Player, PlayerRatingNode, RatingPeriod
from django.urls import reverse
from django.template.defaultfilters import slugify
import json


# Create your views here.
def team_profile(request, player_id):
    player = Player.objects.get(pk=player_id)

    # player_ratings = PlayerRatingNode.objects.filter(player_id=player_id).order_by('-rating_period__end_datetime')[:12]
    player_ratings = PlayerRatingNode.objects.filter(player_id=player_id).order_by('-rating_period__end_datetime')

    ratings_data = [
        round(rating.rating) for rating in player_ratings
    ]

    reversed_ratings_data = list(reversed(ratings_data))

    rating_periods = RatingPeriod.objects.all().order_by('-end_datetime')[:len(reversed_ratings_data)]
    categories = [rp.end_datetime.strftime("%b") for rp in rating_periods]
    reversed_categories = list(reversed(categories))

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
    }

    return render(request, 'teams/team_profile.html', context)
