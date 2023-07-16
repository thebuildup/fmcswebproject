from django.shortcuts import render


# Create your views here.


def ranking_view(request):
    return render(request, 'leaderboard/ranking.html')
