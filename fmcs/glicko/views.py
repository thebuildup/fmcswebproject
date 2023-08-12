from django.shortcuts import render

from .models import Player, PlayerRatingNode


# Create your views here.


def ranking_view(request):
    last_rating_period = PlayerRatingNode.get_last_rating_period()

    if last_rating_period:
        players = Player.objects.filter(playerratingnode__rating_period=last_rating_period,
                                        playerratingnode__is_active=True).order_by('playerratingnode__ranking')
        top_players = players[:3]
    else:
        players = Player.objects.none()
        top_players = []

    context = {
        'top_players': top_players,
        'players': players
    }

    return render(request, 'rating/team_ranking.html', context)


def search_players(request):
    last_rating_period = PlayerRatingNode.get_last_rating_period()

    if last_rating_period:
        keyword = request.GET.get('keyword', '')
        if keyword:
            players = Player.objects.filter(playerratingnode__rating_period=last_rating_period,
                                            playerratingnode__is_active=True, name__icontains=keyword)
        else:
            players = Player.objects.filter(playerratingnode__rating_period=last_rating_period,
                                            playerratingnode__is_active=True).order_by('playerratingnode__ranking')
    else:
        players = Player.objects.none()

    context = {
        'all_players': players,
    }

    return render(request, 'rating/search_results.html', context)
