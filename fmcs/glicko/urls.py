from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.ranking_view, name='fmcs'),
    path('search/', views.search_players, name='search_players'),
    path('players/', views.PlayerViewSet.as_view()),
    path('rating/', views.PlayerRatingNoodeViewSet.as_view()),
    # path('players/', views.PlayerViewSet.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
