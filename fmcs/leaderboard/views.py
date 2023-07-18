from django.shortcuts import render

from .models import Player


# Create your views here.


def ranking_view(request):
    players = Player.objects.all().order_by('playerratingnode__id')

    top_players = players[:3]

    context = {
        'top_players': top_players,
        'players': players
    }

    return render(request, 'leaderboard/team_ranking.html', context)


def search_players(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        players = Player.objects.filter(name__icontains=keyword)
    else:
        players = Player.objects.all().order_by('playerratingnode__ranking')

    context = {
        'all_players': players,
    }

    return render(request, 'leaderboard/search_results.html', context)
