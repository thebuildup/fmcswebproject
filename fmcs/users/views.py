from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login


# Create your views here.
def login_view(request):
    if request.method == "POST":
        if 'new_nickname' in request.POST and request.POST['new_nickname'].strip():
            new_username = request.POST.get('new_nickname')
            new_email = request.POST.get('new_email')
            new_password = request.POST.get('new_password')
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=new_email).exists():
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


def profile(request):
    return render(request, 'profile.html')
