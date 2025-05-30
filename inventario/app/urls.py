from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index, name='index'), # Ruta para la página de inicio
    path('login/', views.login, name='login'), # Ruta para la página de inicio de sesión
    path('register/', views.register, name='register'),# Ruta para la página de registro
    path ('admin/', views.admin, name='admin'), # Ruta para la página de administración
]
