from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
