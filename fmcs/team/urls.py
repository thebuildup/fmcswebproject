from django.urls import path

from . import views

urlpatterns = [
    path('<int:player_id>', views.team_profile, name='team_profile'),
    # path('<str:player_link>', views.team_profile, name='team_profile'),
    # path('<str:(?P<player_link>[^/]+)\\Z>', views.team_profile, name='team_profile'),
]
