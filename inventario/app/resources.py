from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, BooleanWidget, DateWidget
from .models import (
    Equipo, TipoEquipo, TipoAlmacenamiento, Disponibilidad,
    Sucursal, RazonSocial
)

class EquipoResource(resources.ModelResource):
    # Definir campos con widgets personalizados para las relaciones ForeignKey
    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(TipoEquipo, 'nombre_tipo_equipo')
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

    fk_sucursal = fields.Field(
        column_name='sucursal',
        attribute='fk_sucursal',
        widget=ForeignKeyWidget(Sucursal, 'nombre_suc')
    )

    fk_razon_social = fields.Field(
        column_name='razon_social',
        attribute='fk_razon_social',
        widget=ForeignKeyWidget(RazonSocial, 'razon')
    )

    # Campo booleano para licencia_office
    licencia_office = fields.Field(
        column_name='licencia_office',
        attribute='licencia_office',
        widget=BooleanWidget()
    )

    # Campos de fecha
    fecha_de_adquisicion = fields.Field(
        column_name='fecha_adquisicion',
        attribute='fecha_de_adquisicion',
        widget=DateWidget('%Y-%m-%d')  # Formato: YYYY-MM-DD
    )

    class Meta:
        model = Equipo
        # Definir qué campos se pueden importar/exportar
        fields = (
            'id', 'nombre', 'tipo', 'marca', 'modelo', 'numero_serie',
            'fecha_de_adquisicion', 'descripcion',
            'fk_sucursal', 'fk_razon_social', 'tipo_almacenamiento',
            'capacidad_almacenamiento', 'ram', 'procesador',
            'disponibilidad', 'licencia_office', 'version_windows'
        )

        # Campos que se pueden usar para identificar registros existentes
        import_id_fields = ('numero_serie',)

        # Configuraciones adicionales
        skip_unchanged = True
        report_skipped = True
        use_transactions = True

    def before_import_row(self, row, **kwargs):
        """
        Procesar datos antes de importar cada fila
        """
        # Limpiar espacios en blanco
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.strip()

        # Convertir valores vacíos a None
        empty_to_none_fields = [
            'marca', 'modelo', 'numero_serie', 'descripcion',
            'capacidad_almacenamiento', 'ram', 'procesador',
            'version_windows', 'fecha_adquisicion', 'sucursal',
            'razon_social', 'tipo_almacenamiento'
        ]

        for field in empty_to_none_fields:
            if row.get(field) == '' or row.get(field) is None:
                row[field] = None

    def import_obj(self, obj, data, dry_run):
        """
        Procesar el objeto antes de guardarlo
        """
        # Generar nombre automático si está vacío
        if not data.get('nombre'):
            tipo_nombre = data.get('tipo', 'Equipo')
            marca_nombre = data.get('marca', 'Sin marca')
            data['nombre'] = f"{tipo_nombre} - {marca_nombre}"

        # Asignar disponibilidad por defecto si no se especifica
        if not data.get('disponibilidad'):
            try:
                disponible = Disponibilidad.objects.get(nombre='Disponible')
                obj.disponibilidad = disponible
            except Disponibilidad.DoesNotExist:
                pass

        return super().import_obj(obj, data, dry_run)