from django.shortcuts import render


# Create your views here.
def team_profile(request):
    return render(request, 'teams/team_profile.html')
