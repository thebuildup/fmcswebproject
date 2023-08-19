from django.urls import path

from . import views

urlpatterns = [
    path('<str:formatted_player_name>', views.team_profile, name='team_profile'),
    # path('<str:player_name>', views.team_test_profile, name='team_test_profile'),
    # path('<str:formatted_player_name>', views.team_test_profile, name='team_test_profile'),
    # path('<str:(?P<player_link>[^/]+)\\Z>', views.team_profile, name='team_profile'),
]
