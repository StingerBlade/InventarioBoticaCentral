from django.contrib import admin
from .models import (
    Estado, Municipio, Sucursal, Departamento, RazonSocial, TipoEquipo,
    TipoAlmacenamiento, Disponibilidad, Empleado, Equipo, Mantenimiento,
    Prestamo, DispositivoMovil
)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_empleado', 'correo', 'puesto', 'fk_departamento', 'fk_sucursal')
    search_fields = ('nombre_empleado', 'correo', 'puesto', 'fk_departamento__nombre')
    list_filter = ('fk_departamento', 'fk_sucursal')

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'marca', 'modelo', 'fk_sucursal', 'disponibilidad')
    search_fields = ('nombre', 'marca', 'modelo', 'numero_serie')
    list_filter = ('disponibilidad', 'tipo', 'marca', 'fk_sucursal')
    ordering = ('nombre',)

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('fk_equipo', 'fk_empleado', 'fecha_prestamo', 'fecha_devolucion')
    search_fields = (
        'fk_equipo__nombre', 'fk_equipo__marca', 'fk_equipo__modelo',
        'fk_empleado__nombre_empleado', 'fk_razon_social__razon'
    )
    list_filter = ('fk_equipo__tipo', 'fk_equipo__marca', 'fk_equipo__fk_sucursal')

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_suc', 'fk_municipio')
    search_fields = ('nombre_suc',)
    ordering = ('nombre_suc',)

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre_mun', 'fk_estado')
    search_fields = ('nombre_mu',)
    ordering = ('nombre_mun',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_est',)
    search_fields = ('nombre_est',)
    ordering = ('nombre_est',)
# Registrar los demás modelos directamente

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('fk_equipo', 'fecha', 'tecnico', 'estatus')
    search_fields = ('fk_equipo__nombre', 'tecnico', 'estatus')
    list_filter = ('estatus',)
    ordering = ('fecha',)
    
admin.site.register(Departamento)
admin.site.register(RazonSocial)
admin.site.register(TipoEquipo)
admin.site.register(TipoAlmacenamiento)
admin.site.register(Disponibilidad)

admin.site.register(DispositivoMovil)


admin.site.site_header = "Inventario - BOTICA CENTRAL"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Sistema de Inventario"
