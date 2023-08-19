from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from glicko.models import Player
from .models import Profile
import re


# Create your views here.

def remove_dots_from_email(email):
    # Удаляем все точки из email-адреса
    return email.replace('.', '')


def is_valid_username(username):
    # Проверяем, что имя пользователя состоит только из букв, цифр и подчеркивания
    # и не содержит пробелов или знаков, которые могли бы использоваться для SQL-инъекций
    if re.match(r'^[\w.@+-]+$', username):
        return True
    return False


def login_view(request):
    if request.method == "POST":
        if 'new_nickname' in request.POST and request.POST['new_nickname'].strip():
            new_username = request.POST.get('new_nickname')
            new_email = request.POST.get('new_email')
            new_password = request.POST.get('new_password')

            # Удаляем точки из email-адреса перед проверкой на уникальность
            clean_email = remove_dots_from_email(new_email)

            if not is_valid_username(new_username):
                messages.error(request, "Invalid characters in username")
            elif User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=clean_email).exists():
                messages.error(request, "Email already exists")
            else:
                new_user = User.objects.create_user(new_username, new_email, new_password)
                new_user.save()
                user = authenticate(request, username=new_username, password=new_password)
                login(request, user)
                return redirect('home')
        else:
            username = request.POST.get('nickname')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    context = {'error': messages.get_messages(request)}
    return render(request, 'login.html', context)


def profile(request, username):
    username = get_object_or_404(User, username=username)

    try:
        player = Player.objects.get(user=username.id)
    except Player.DoesNotExist:
        player = None

    profile = Profile.objects.get(user=username.id)

    try:
        discord = profile.discord
    except:
        discord = None

    try:
        twitter_link = profile.twitter  # Получаем полную ссылку на Twitter профиль
        twitter_username = twitter_link.split("/")[-1]  # Разделяем по "/" и берем последний элемент
    except:
        twitter_username = None

    try:
        telegram_link = profile.telegram  # Получаем полную ссылку на Twitter профиль
        telegram_username = telegram_link.split("/")[-1]  # Разделяем по "/" и берем последний элемент
    except:
        telegram_username = None

    try:
        country = profile.country
    except:
        country = None

    return render(request, 'user_profile.html', {
        'username': username,
        'player': player,
        'profile': profile,
        'discord': discord,
        'twitter_username': twitter_username,
        'telegram_username': telegram_username,
        'country': country,
    })
