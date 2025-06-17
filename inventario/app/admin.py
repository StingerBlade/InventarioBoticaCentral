from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import EquipoResource  # Importar el resource que creamos

from .models import (
    Estado, Municipio, Sucursal, Departamento, RazonSocial, TipoEquipo,
    TipoAlmacenamiento, Disponibilidad, Empleado, Equipo, Mantenimiento,
    Prestamo, DispositivoMovil, Tipo_Sucursal, Asignacion
)
from .inlines import MantenimientoInline, AsignacionInline, PrestamoInline

admin.site.site_header = "Inventario - BOTICA CENTRAL"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Sistema de Inventario"




@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_empleado', 'correo', 'puesto', 'fk_departamento', 'fk_sucursal')
    search_fields = ('nombre_empleado', 'correo', 'puesto', 'fk_departamento__nombre')
    list_filter = ('fk_departamento', 'fk_sucursal')
    ordering = ('nombre_empleado',)
    inlines = [AsignacionInline, PrestamoInline]



# CLASE ACTUALIZADA CON IMPORT/EXPORT
@admin.register(Equipo)
class EquipoAdmin(ImportExportModelAdmin):  # Cambiar ExportMixin por ImportExportModelAdmin
    resource_class = EquipoResource  # Agregar esta línea

    list_display = ('nombre', 'tipo', 'marca', 'modelo', 'fk_sucursal', 'disponibilidad', 'fecha_de_alta', 'fecha_de_adquisicion')
    search_fields = ('nombre', 'marca', 'modelo', 'numero_serie')
    list_filter = ('disponibilidad', 'tipo', 'fk_sucursal')
    ordering = ('nombre',)
    inlines = [MantenimientoInline]
    fieldsets = (
        ('Datos generales', {
            'fields': ('nombre', 'tipo', 'marca', 'modelo', 'numero_serie', 'fecha_de_adquisicion')
        }),
        ('Especificaciones técnicas', {
            'fields': ('ram', 'procesador', 'tipo_almacenamiento', 'capacidad_almacenamiento', 'version_windows')
        }),
        ('Ubicación y estado', {
            'fields': ('fk_sucursal', 'fk_razon_social', 'disponibilidad')
        }),
        ('Otros', {
            'fields': ('licencia_office', 'descripcion')
        }),
    )
    date_hierarchy='fecha_de_adquisicion'

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    search_fields = ('nombre_suc',)
    ordering = ('nombre_suc',)
    list_filter = ('fk_municipio__nombre_mun', 'fk_tipo_sucursal','fk_razon_social')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('fk_equipo', 'fk_empleado', 'fecha_prestamo', 'fecha_devolucion')
    search_fields = (
        'fk_equipo__nombre', 'fk_equipo__marca', 'fk_equipo__modelo',
        'fk_empleado__nombre_empleado'
    )
    list_filter = ('fk_equipo__tipo',  'fk_equipo__fk_sucursal')

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('fk_equipo', 'fk_empleado', 'fecha_asignacion', 'fecha_devolucion')
    search_fields = (
        'fk_equipo__nombre', 'fk_equipo__marca', 'fk_equipo__modelo',
        'fk_empleado__nombre_empleado'
    )
    list_filter = ('fk_equipo__tipo',  'fk_equipo__fk_sucursal')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre_mun', 'fk_estado')
    search_fields = ('nombre_mun',)  # Corregido el typo
    ordering = ('nombre_mun',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_est',)
    search_fields = ('nombre_est',)
    ordering = ('nombre_est',)

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('fk_equipo', 'fecha', 'tecnico', 'estatus', 'tipo_mantenimiento', 'tipo_general')
    search_fields = ('fk_equipo__nombre', 'tecnico', 'estatus', 'tipo_mantenimiento__nombre')
    list_filter = ('estatus', 'tipo_mantenimiento__padre__padre__nombre')
    ordering = ('fecha',)
    date_hierarchy = 'fecha'

    def tipo_general(self, obj):
        return obj.tipo_general
    tipo_general.short_description = 'Tipo General'

@admin.register(Tipo_Sucursal)
class TipoSucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_sucursal',)
    search_fields = ('nombre_tipo_sucursal',)
    ordering = ('nombre_tipo_sucursal',)

# Registrar los demás modelos directamente
admin.site.register(Departamento)
admin.site.register(RazonSocial)
admin.site.register(TipoEquipo)
admin.site.register(TipoAlmacenamiento)
admin.site.register(Disponibilidad)
admin.site.register(DispositivoMovil)