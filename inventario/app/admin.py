from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import EquipoResource  # Importar el resource que creamos
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import (
    Estado, Municipio, Sucursal, Departamento, RazonSocial, TipoEquipo,
    TipoAlmacenamiento, Disponibilidad, Empleado, Equipo, Mantenimiento,
    Prestamo, DispositivoMovil, Tipo_Sucursal, Asignacion, EquipoEliminado
)
from .inlines import MantenimientoInline, AsignacionInline, PrestamoInline
from .resources import AsignacionResource
admin.site.site_header = "Inventario - BOTICA CENTRAL"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Sistema de Inventario"

# Agregar esto a tu admin.py existente

@admin.register(EquipoEliminado)
class EquipoEliminadoAdmin(admin.ModelAdmin):
    list_display = (
        'equipo_id_original', 
        'nombre', 
        'marca', 
        'modelo', 
        'tipo_equipo_nombre',
        'sucursal_nombre', 
        'fecha_eliminacion', 
        'usuario_eliminacion'
    )
    
    list_filter = (
        'fecha_eliminacion',
        'tipo_equipo_nombre',
        'sucursal_nombre',
        'razon_social_nombre',
        'disponibilidad_nombre',
        'usuario_eliminacion'
    )
    
    search_fields = (
        'nombre', 
        'marca', 
        'modelo', 
        'numero_serie',
        'equipo_id_original',
        'usuario_eliminacion'
    )
    
    readonly_fields = (
        'equipo_id_original',
        'nombre',
        'fecha_de_adquisicion',
        'fecha_de_alta',
        'marca',
        'modelo',
        'numero_serie',
        'descripcion',
        'capacidad_almacenamiento',
        'ram',
        'procesador',
        'folio',
        'rfc',
        'tipo_equipo_nombre',
        'sucursal_nombre',
        'razon_social_nombre',
        'tipo_almacenamiento_nombre',
        'disponibilidad_nombre',
        'fecha_eliminacion',
        'datos_completos'
    )
    
    fieldsets = (
        ('Información del Equipo Eliminado', {
            'fields': (
                'equipo_id_original',
                'nombre',
                'tipo_equipo_nombre',
                'marca',
                'modelo',
                'numero_serie'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_de_adquisicion',
                'fecha_de_alta',
                'fecha_eliminacion'
            )
        }),
        ('Especificaciones Técnicas', {
            'fields': (
                'ram',
                'procesador',
                'tipo_almacenamiento_nombre',
                'capacidad_almacenamiento'
            ),
            'classes': ('collapse',)
        }),
        ('Ubicación Original', {
            'fields': (
                'sucursal_nombre',
                'razon_social_nombre',
                'disponibilidad_nombre'
            )
        }),
        ('Información de Eliminación', {
            'fields': (
                'usuario_eliminacion',
                'motivo_eliminacion'
            ),
            'classes': ('wide',)
        }),
        ('Proveedor', {
            'fields': (
                'folio',
                'rfc'
            ),
            'classes': ('collapse',)
        }),
        ('Otros Datos', {
            'fields': (
                'descripcion',
                'datos_completos'
            ),
            'classes': ('collapse',)
        })
    )
    
    ordering = ('-fecha_eliminacion',)
    date_hierarchy = 'fecha_eliminacion'
    
    # Deshabilitar agregar nuevos registros (solo se crean automáticamente)
    def has_add_permission(self, request):
        return False
    
    # Deshabilitar edición (solo lectura)
    def has_change_permission(self, request, obj=None):
        return True  # Permitir ver, pero campos son readonly
    
    # Opcional: permitir eliminar registros muy antiguos
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    # Método para mostrar datos JSON de forma más legible
    def datos_completos_formatted(self, obj):
        if obj.datos_completos:
            import json
            return format_html(
                '<pre>{}</pre>', 
                json.dumps(obj.datos_completos, indent=2, ensure_ascii=False)
            )
        return "Sin datos adicionales"
    datos_completos_formatted.short_description = 'Datos Completos'
    
    # Agregar acción personalizada para restaurar equipos (opcional)
    actions = ['restaurar_equipos']
    
    def restaurar_equipos(self, request, queryset):
        """
        Acción personalizada para restaurar equipos eliminados
        """
        count = 0
        for equipo_eliminado in queryset:
            # Aquí podrías implementar la lógica para restaurar
            # Por ahora solo mostramos un mensaje
            count += 1
        
        self.message_user(
            request,
            f'Se seleccionaron {count} equipos. '
            'La funcionalidad de restauración debe implementarse según tus necesidades.'
        )
    restaurar_equipos.short_description = "Marcar para restauración"

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
    def delete_model(self, request, obj):
        # Guarda el usuario y motivo antes de eliminar
        obj._usuario_eliminacion = request.user.username
        obj._motivo_eliminacion = f"Eliminado por {request.user.username} desde el admin"
        obj.save()
        super().delete_model(request, obj)
        
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
        ('Proveedor', {
            'fields': ('folio', 'rfc')
        })
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
class AsignacionAdmin(ImportExportModelAdmin):
    resource_class = AsignacionResource  # Agregar esta línea
    
    list_display = ('fk_equipo', 'fk_empleado', 'fecha_asignacion', 'fecha_devolucion')
    search_fields = (
        'fk_equipo__nombre', 'fk_equipo__marca', 'fk_equipo__modelo',
        'fk_empleado__nombre_empleado'
    )
    list_filter = ('fk_equipo__tipo', 'fk_equipo__fk_sucursal')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('custom-action/', self.custom_action, name='asignacion_custom_action'),
        ]
        return custom_urls + urls

    def custom_action(self, request):
        return HttpResponseRedirect('https://responsivas.vercel.app')
    
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