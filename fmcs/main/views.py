from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.


def index(request):
    # return HttpRequest("<h4>Hello</h4>")
    return render(request, 'main/index.html')

# def registr(request):
#     return render(request, 'main/registration.html')
