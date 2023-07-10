from django.shortcuts import render

from .models import Event, Organizator


# Create your views here.
def event_view(request):
    events_list = Event.objects.all()
    reversed_events_list = [event for event in reversed(events_list)]
    event_list_filter = Event.objects.filter(status_name__status_name__in=["Active", "Starting Soon"])
    carousel_list = [event for event in reversed(event_list_filter)]
    org_list = Organizator.objects.all()
    context = {
        'events_list': reversed_events_list,
        'org_list': org_list,
        'carousel_list': carousel_list,
    }

    return render(request, 'leaderboard/explore.html', context=context)
