from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import  messages
from django.contrib.auth import  authenticate, login
# Create your views here.

def hello (request):
    return HttpResponse("Hello, world. You're at the app index.")

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contra']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect (administracion)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')
def register(request):
    return render(request, 'register.html')

def administracion(request):
    return render(request, 'admin.html')
