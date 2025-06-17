from import_export.admin import ExportMixin
from django.contrib import admin
from .models import Mantenimiento, Empleado, Equipo, Prestamo, Asignacion

class PrestamoInline(admin.TabularInline):
    model = Prestamo
    extra = 1

class AsignacionInline(admin.TabularInline):
    model = Asignacion
    extra = 1

class MantenimientoInline(admin.TabularInline):
    model = Mantenimiento
    extra = 1