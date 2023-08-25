from django.urls import path

from . import views

urlpatterns = [
    path('', views.ranking_page, name='ranking_page'),
]
