from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('<str:username>/', views.profile, name='user_profile'),
]
