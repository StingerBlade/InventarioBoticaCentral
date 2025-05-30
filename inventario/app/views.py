from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

def hello (request):
    return HttpResponse("Hello, world. You're at the app index.")

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def admin(request):
    return render(request, 'admin.html')
