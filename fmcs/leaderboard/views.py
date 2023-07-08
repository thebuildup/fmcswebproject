from django.shortcuts import render

from .models import Event


# Create your views here.
def event_view(request):
    events_list = Event.objects.all()

    context = {
        'events_list': events_list
    }

    return render(request, 'leaderboard/explore.html', context=context)
