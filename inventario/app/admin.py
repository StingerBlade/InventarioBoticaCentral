from django.contrib import admin
from .models import (
    Estado, Municipio, Sucursal, RazonSocial, TipoEquipo, Empleado,
    Equipo, Mantenimiento, Prestamo, DispositivoMovil
)
from .models import TipoAlmacenamiento, Disponibilidad, Departamento

admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Sucursal)
admin.site.register(RazonSocial)
admin.site.register(TipoEquipo)
admin.site.register(Empleado)
admin.site.register(Equipo)
admin.site.register(Mantenimiento)
admin.site.register(Prestamo)
admin.site.register(DispositivoMovil)
admin.site.register(TipoAlmacenamiento)
admin.site.register(Disponibilidad)

admin.site.register(Departamento)


admin.site.site_header = "Inventario - BOTICA CENTRAL"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Sistema de Inventario"

