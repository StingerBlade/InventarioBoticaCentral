from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import  messages
from django.contrib.auth import  authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def hello (request):
    return HttpResponse("Hello, world. You're at the app index.")
@login_required(login_url='login_view') 
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contra']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('administracion')
        else:
            return redirect('login_view')
        
    return render(request, 'login.html')
def register(request):
    return render(request, 'register.html')
@login_required(login_url='login_view') 
def administracion(request):
    return render(request, 'admin.html')
