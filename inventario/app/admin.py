from django.contrib import admin
from .models import (
    Estado, Municipio, Sucursal, RazonSocial, TipoEquipo, Empleado,
    Equipo, Mantenimiento, Prestamo, DispositivoMovil
)


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
