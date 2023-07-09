from django.shortcuts import render

from .models import Event, Organizator


# Create your views here.
def event_view(request):
    events_list = Event.objects.all()
    org_list = Organizator.objects.all()
    context = {
        'events_list': events_list,
        'org_list': org_list
    }

    return render(request, 'leaderboard/explore.html', context=context)
