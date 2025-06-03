from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index, name='index'), # Ruta para la página de inicio
    path('login_view/', views.login_view, name='login_view'), # Ruta para la página de inicio de sesión
    path('register/', views.register, name='register'),# Ruta para la página de registro
    path ('administracion/', views.administracion, name='administracion'), # Ruta para la página de administración
]
