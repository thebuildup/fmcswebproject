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


# def register_request(request):
#     # if not Group.objects.filter(name='Managers').exists():
#     #     Group.objects.create(name='Managers')
#     #
#     # customer_group = Group.objects.get(name='Managers')
#     if request.method == "POST":
#         new_username = request.POST.get('new_nickname')
#         new_email = request.POST.get('new_email')
#         new_password = request.POST.get('new_password')
#         print(new_username)
#         print(new_email)
#         print(new_password)
#         # Проверка, что все поля заполнены
#         # if not new_username or not new_email or not new_password:
#         #     return render(request, 'login.html', {'error': 'Please fill all fields'})
#
#         # Создание нового пользователя
#         new_user = User.objects.create_user(new_username, new_email, new_password)
#         new_user.save()
#         return redirect('home')
#     return render(request, 'home')

def profile(request):
    return render(request, 'profile.html')
