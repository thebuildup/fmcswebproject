from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_view, name='events'),
    path('create/', views.create_tournament, name='create_tournament'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    # path('<int:tournament_id>/', views.add_participant, name='add_participant'),
    path('<int:tournament_id>/delete_participant/<int:participant_id>/', views.delete_participant,
         name='delete_participant'),
    path('list/', views.tournament_list, name='tournament_list'),
    path('<int:tournament_id>/get_participants_data/', views.get_participants_data, name='get_participants_data'),
    # Другие URL-шаблоны для других представлений, если необходимо
]
