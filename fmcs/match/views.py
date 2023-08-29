from django.shortcuts import render, redirect, get_object_or_404
from glicko.models import Match


# Create your views here.
def match_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    context = {
        'match': match
    }
    return render(request, 'match_detail.html', context)
