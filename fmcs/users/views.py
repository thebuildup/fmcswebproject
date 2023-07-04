from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
# from.forms import CustomAuthenticationForm


# @login_required
# def home(request):
#     return render(request, 'home.html')

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        user = authenticate(request, username=nickname, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error")
    return render(request, 'login.html')

# Create your views here.
