from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_view, name='events'),
]
