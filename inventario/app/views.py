from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import  messages
from django.contrib.auth import  authenticate, login
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from .models import Equipo
# Create your views here.

def hello (request):
    return HttpResponse("Hello, world. You're at the app index.")

def index(request):
    return redirect('/admin/')

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

def exportar_equipos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Equipos"

    # Cabeceras de las columnas
    ws.append([
        'Nombre',
        'Tipo de Equipo',
        'Marca',
        'Modelo',
        'Número de Serie',
        'Sucursal',
        'Disponibilidad',
        'RAM (GB)',
        'Procesador',
        'Versión de Windows'
    ])

    # Datos
    for equipo in Equipo.objects.all():
        ws.append([
            equipo.nombre,
            equipo.tipo.nombre_tipo_equipo if equipo.tipo else '',
            equipo.marca or '',
            equipo.modelo or '',
            equipo.numero_serie or '',
            equipo.fk_sucursal.nombre_suc if equipo.fk_sucursal else '',
            equipo.disponibilidad.nombre if equipo.disponibilidad else '',
            equipo.ram or '',
            equipo.procesador or '',
            equipo.version_windows or '',
        ])

    # Generar archivo
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Reporte_Equipos.xlsx'
    wb.save(response)
    return response

