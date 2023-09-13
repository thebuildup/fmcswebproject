from django.shortcuts import render
from rest_framework import generics
from . import serializers
from .models import Player, PlayerRatingNode
from rest_framework import viewsets


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


# class PlayerViewSet(viewsets.ModelViewSet):
#     """A viewset for players."""
#
#     queryset = Player.objects.all()
#     http_method_names = ["get", "post", "patch"]
#     serializer_class = serializers.PlayerSerializer

class PlayerViewSet(generics.ListAPIView):
    """A viewset for players."""

    queryset = Player.objects.all()
    http_method_names = ["get"]
    serializer_class = serializers.PlayerSerializer


class PlayerRatingNoodeViewSet(generics.ListAPIView):
    """A viewset for players."""
    last_rating_period = PlayerRatingNode.get_last_rating_period()
    queryset = PlayerRatingNode.objects.filter(playerratingnode__rating_period=last_rating_period,
                                               playerratingnode__is_active=True).order_by('playerratingnode__ranking')
    http_method_names = ["get"]
    serializer_class = serializers.PlayerRatingNodeSerializer
