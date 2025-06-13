from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, BooleanWidget, DateWidget
from .models import (
    Equipo, TipoEquipo, Sucursal, RazonSocial,
    TipoAlmacenamiento, Disponibilidad
)
from .inlines import MantenimientoInline


class EquipoResource(resources.ModelResource):
    # Configurar campos con ForeignKey para que acepten nombres en lugar de IDs
    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(TipoEquipo, 'nombre_tipo_equipo')
    )

    sucursal = fields.Field(
        column_name='sucursal',
        attribute='fk_sucursal',
        widget=ForeignKeyWidget(Sucursal, 'nombre_suc')
    )

    razon_social = fields.Field(
        column_name='razon_social',
        attribute='fk_razon_social',
        widget=ForeignKeyWidget(RazonSocial, 'razon')
    )

    tipo_almacenamiento = fields.Field(
        column_name='tipo_almacenamiento',
        attribute='tipo_almacenamiento',
        widget=ForeignKeyWidget(TipoAlmacenamiento, 'nombre')
    )

    disponibilidad = fields.Field(
        column_name='disponibilidad',
        attribute='disponibilidad',
        widget=ForeignKeyWidget(Disponibilidad, 'nombre')
    )

    # Configurar campos boolean y fecha
    licencia_office = fields.Field(
        column_name='licencia_office',
        attribute='licencia_office',
        widget=BooleanWidget()
    )

    fecha_de_adquisicion = fields.Field(
        column_name='fecha_de_adquisicion',
        attribute='fecha_de_adquisicion',
        widget=DateWidget('%Y-%m-%d')  # Formato: YYYY-MM-DD
    )

    class Meta:
        model = Equipo
        # Especificar qué campos importar
        fields = (
            'id', 'nombre', 'fecha_de_adquisicion', 'tipo', 'marca',
            'modelo', 'numero_serie', 'descripcion', 'sucursal',
            'razon_social', 'tipo_almacenamiento', 'capacidad_almacenamiento',
            'ram', 'procesador', 'disponibilidad', 'licencia_office',
            'version_windows'
        )
        export_order = fields
        import_id_fields = ('numero_serie',)  # Usar número de serie como identificador único
        skip_unchanged = True
        report_skipped = False

    def before_import_row(self, row, **kwargs):
        """
        Procesar datos antes de importar cada fila
        """
        # Limpiar espacios en blanco
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()

        # Convertir valores boolean
        if 'licencia_office' in row:
            licencia_val = str(row['licencia_office']).lower()
            if licencia_val in ['si', 'sí', 'yes', '1', 'true', 'verdadero']:
                row['licencia_office'] = True
            else:
                row['licencia_office'] = False

    def skip_row(self, instance, original, row, import_validation_errors=None):
        """
        Decidir si saltar una fila durante la importación
        """
        # Saltar filas sin nombre o tipo
        if not row.get('nombre') or not row.get('tipo'):
            return True
        return super().skip_row(instance, original, row, import_validation_errors)


# 2. ACTUALIZAR EL ADMIN.PY
# inventario/app/admin.py (agregar estas líneas)

from import_export.admin import ImportExportModelAdmin
# También importar tu resource
from .resources import EquipoResource


# 3. EJEMPLO DE ARCHIVO CSV PARA IMPORTAR
# equipos_ejemplo.csv

"""
nombre,tipo,marca,modelo,numero_serie,fecha_de_adquisicion,sucursal,razon_social,tipo_almacenamiento,capacidad_almacenamiento,ram,procesador,disponibilidad,licencia_office,version_windows,descripcion
Laptop Dell 001,Laptop,Dell,Inspiron 15,DL123456789,2024-01-15,Sucursal Centro,BOTICA CENTRAL SA DE CV,SSD,512,8,Intel i5-12400,Disponible,Si,Windows 11,Laptop para área administrativa
Desktop HP 002,Desktop,HP,EliteDesk 800,HP987654321,2024-02-20,Sucursal Norte,BOTICA CENTRAL SA DE CV,HDD,1000,16,Intel i7-12700,Disponible,No,Windows 10,Computadora de escritorio para contabilidad
Tablet Samsung 003,Tablet,Samsung,Galaxy Tab A8,SM12345678,2024-03-10,Sucursal Sur,BOTICA CENTRAL SA DE CV,,64,4,Snapdragon 662,En préstamo,No,,Tablet para inventarios móviles
"""

# 4. PASOS PARA USAR LA IMPORTACIÓN:

# 1. Accede al admin de Django (http://localhost:8000/admin/)
# 2. Ve a la sección "Equipos"
# 3. Verás botones "Import" y "Export" en la parte superior
# 4. Haz clic en "Import"
# 5. Selecciona tu archivo CSV o Excel
# 6. Revisa la vista previa
# 7. Confirma la importación

# 5. FORMATO REQUERIDO PARA FECHAS:
# - Usar formato YYYY-MM-DD (ejemplo: 2024-01-15)
# - Para licencia_office: usar "Si", "No", "True", "False", "1", "0"

# 6. CAMPOS OBLIGATORIOS EN EL CSV:
# - nombre: Nombre del equipo
# - tipo: Debe coincidir exactamente con un TipoEquipo existente
# - sucursal: Debe coincidir con el nombre de una Sucursal existente
# - disponibilidad: Debe coincidir con un estado de Disponibilidad existente

# 7. PARA CREAR TIPOS DE DATOS FALTANTES:
# Antes de importar equipos, asegúrate de tener creados:
# - TipoEquipo (Laptop, Desktop, Tablet, etc.)
# - Sucursal (con sus respectivos municipios)
# - RazonSocial
# - TipoAlmacenamiento (SSD, HDD, etc.)
# - Disponibilidad (Disponible, En préstamo, En reparación, etc.)

# 8. COMANDO PARA EXPORTAR TEMPLATE:
# python manage.py shell
# from app.resources import EquipoResource
# resource = EquipoResource()
# dataset = resource.export()
# with open('template_equipos.csv', 'w', encoding='utf-8') as f:
#     f.write(dataset.csv)