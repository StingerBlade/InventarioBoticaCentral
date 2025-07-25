from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, BooleanWidget, DateWidget
from datetime import datetime
from .models import (
    Equipo, TipoEquipo, TipoAlmacenamiento, Disponibilidad,
    Sucursal, RazonSocial, Asignacion, Empleado, Departamento
)

class AsignacionResource(resources.ModelResource):
    # Campos personalizados para mostrar nombres en lugar de IDs
    empleado_nombre = fields.Field(
        column_name='Empleado',
        attribute='fk_empleado',
        widget=ForeignKeyWidget(Empleado, 'nombre_empleado')
    )
    
    equipo_nombre = fields.Field(
        column_name='Equipo',
        attribute='fk_equipo',
        widget=ForeignKeyWidget(Equipo, 'nombre')
    )
    
    class Meta:
        model = Asignacion
        fields = (
            'id',
            'empleado_nombre',
            'equipo_nombre', 
            'fecha_asignacion',
            'fecha_devolucion'
        )
        export_order = (
            'id',
            'empleado_nombre',
            'equipo_nombre',
            'fecha_asignacion',
            'fecha_devolucion'
        )

class FlexibleDateWidget(DateWidget):
    """Widget de fecha que maneja fechas de Excel correctamente"""

    def clean(self, value, row=None, **kwargs):
        # Si está vacío o es None, devolver None
        if not value or value == '':
            return None

        # Si ya es un objeto datetime (típico en Excel), convertir a date
        if isinstance(value, datetime):
            return value.date()

        # Si es fecha de Python, devolverla directamente
        if hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            return value

        # Si es string, limpiar y procesar
        if isinstance(value, str):
            value = value.strip()
            if not value or value.lower() in ['', 'null', 'none', 'n/a']:
                return None

        # Para todo lo demás, usar el método padre
        return super().clean(value, row, **kwargs)

class EquipoResource(resources.ModelResource):

    # Date field con widget mejorado
    fecha_de_adquisicion = fields.Field(
        column_name='fecha_adquisicion',  # Coincide con el Excel
        attribute='fecha_de_adquisicion',
        widget=FlexibleDateWidget()
    )

    # ForeignKey fields - CORREGIDOS para coincidir con los headers del Excel
    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(TipoEquipo, 'nombre_tipo_equipo')
    )

    # CORRECCIÓN 1: Cambiar column_name para que coincida con el Excel
    fk_sucursal = fields.Field(
        column_name='fk_sucursal',  # Era 'sucursal', ahora coincide con Excel
        attribute='fk_sucursal',
        widget=ForeignKeyWidget(Sucursal, 'nombre_suc')
    )

    # CORRECCIÓN 2: Cambiar column_name para que coincida con el Excel
    fk_razon_social = fields.Field(
        column_name='fk_razon_social',  # Era 'razon_social', ahora coincide con Excel
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

    # Boolean field
    licencia_office = fields.Field(
        column_name='licencia_office',
        attribute='licencia_office',
        widget=BooleanWidget()
    )

    # NUEVOS CAMPOS AGREGADOS: folio y rfc
    folio = fields.Field(
        column_name='folio',
        attribute='folio'
    )

    rfc = fields.Field(
        column_name='rfc',
        attribute='rfc'
    )

    class Meta:
        model = Equipo
        fields = (
            'id',
            # Datos básicos del equipo
            'tipo', 'marca', 'modelo', 'numero_serie',
            # ForeignKeys independientes
            'fk_razon_social', 'fk_sucursal', 'disponibilidad',
            'tipo_almacenamiento',
            # Fecha importante
            'fecha_de_adquisicion',
            # Especificaciones técnicas
            'capacidad_almacenamiento', 'ram', 'procesador',
            'version_windows', 'licencia_office',
            # Datos Proveedor (NUEVOS CAMPOS)
            'folio', 'rfc',
            # Campos opcionales
            'nombre', 'descripcion'
        )
        import_id_fields = ('numero_serie',)
        skip_unchanged = True
        report_skipped = True
        use_transactions = True

    def before_import_row(self, row, **kwargs):
        """Procesar datos antes de importar cada fila"""

        print(f"\n=== PROCESANDO FILA ===")

        # Debug: mostrar valores específicos de Foreign Keys
        print(f"Sucursal: '{row.get('fk_sucursal')}' (tipo: {type(row.get('fk_sucursal'))})")
        print(f"Razón Social: '{row.get('fk_razon_social')}' (tipo: {type(row.get('fk_razon_social'))})")

        # Limpiar espacios en blanco y valores vacíos
        for key, value in row.items():
            if isinstance(value, str):
                cleaned_value = value.strip()
                row[key] = cleaned_value if cleaned_value else None
            elif value == '':
                row[key] = None

        # Campos que pueden estar vacíos (INCLUIR folio y rfc)
        empty_to_none_fields = [
            'marca', 'modelo', 'numero_serie', 'descripcion',
            'capacidad_almacenamiento', 'ram', 'procesador',
            'version_windows', 'fecha_adquisicion', 'fk_sucursal',
            'fk_razon_social', 'tipo_almacenamiento', 'folio', 'rfc'
        ]

        for field in empty_to_none_fields:
            if row.get(field) in ['', None, 'NULL', 'null', 'N/A', 'n/a']:
                row[field] = None

        # Debug: mostrar valores después del procesamiento
        print(f"Sucursal procesada: '{row.get('fk_sucursal')}'")
        print(f"Razón Social procesada: '{row.get('fk_razon_social')}'")
        print(f"Folio procesado: '{row.get('folio')}'")
        print(f"RFC procesado: '{row.get('rfc')}'")
        print("=== FIN PROCESAMIENTO FILA ===\n")

    def import_obj(self, obj, data, dry_run):
        """Procesar el objeto antes de guardarlo"""

        # Debug adicional para Foreign Keys
        print(f"\n--- IMPORT_OBJ DEBUG ---")
        print(f"Datos recibidos para FKs:")
        print(f"  fk_sucursal: {data.get('fk_sucursal')}")
        print(f"  fk_razon_social: {data.get('fk_razon_social')}")
        print(f"  folio: {data.get('folio')}")
        print(f"  rfc: {data.get('rfc')}")

        # Verificar si los objetos relacionados existen
        if data.get('fk_sucursal'):
            try:
                sucursal = Sucursal.objects.get(nombre_suc=data.get('fk_sucursal'))
                print(f"  ✓ Sucursal encontrada: {sucursal}")
            except Sucursal.DoesNotExist:
                print(f"  ✗ Sucursal NO encontrada: {data.get('fk_sucursal')}")
                print(f"  Sucursales disponibles: {list(Sucursal.objects.values_list('nombre_suc', flat=True))}")

        if data.get('fk_razon_social'):
            try:
                razon = RazonSocial.objects.get(razon=data.get('fk_razon_social'))
                print(f"  ✓ Razón Social encontrada: {razon}")
            except RazonSocial.DoesNotExist:
                print(f"  ✗ Razón Social NO encontrada: {data.get('fk_razon_social')}")
                print(f"  Razones sociales disponibles: {list(RazonSocial.objects.values_list('razon', flat=True))}")

        print("--- FIN IMPORT_OBJ DEBUG ---\n")

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


    def before_save_instance(self, *args, **kwargs):
        instance = args[0]  # Primer argumento siempre es la instancia

        try:
            disponible = Disponibilidad.objects.get(nombre='Disponible')
            instance.disponibilidad = disponible
            print(f"✓ Disponibilidad asignada desde before_save_instance: {disponible}")
        except Disponibilidad.DoesNotExist:
            print("⚠️ Disponibilidad 'Disponible' no encontrada")





    def after_import_row(self, row, row_result, **kwargs):
        """Procesar después de importar cada fila (para debug)"""
        if row_result.errors:
            print(f"Errores en fila: {row_result.errors}")
        if hasattr(row_result, 'object_repr'):
            print(f"Objeto procesado: {row_result.object_repr}")



class EmpleadoResource(resources.ModelResource):
    # ForeignKey fields con nombres descriptivos

    nombre_empleado = fields.Field(
        column_name='nombre_empleado',
        attribute='nombre_empleado'
    )

    correo = fields.Field(
        column_name='correo',
        attribute='correo'
    )


    fk_departamento = fields.Field(
        column_name='fk_departamento',
        attribute='fk_departamento',
        widget=ForeignKeyWidget(Departamento, 'nombre')
    )
    
    fk_sucursal = fields.Field(
        column_name='fk_sucursal',
        attribute='fk_sucursal',
        widget=ForeignKeyWidget(Sucursal, 'nombre_suc')
    )
    
    class Meta:
        model = Empleado
        fields = (
            'id',
            'nombre_empleado',
            'correo',
            'fk_sucursal',
            'fk_departamento',
            'puesto',
            )
        export_order = (
            'id',
            'nombre_empleado',
            'correo',
            'fk_sucursal',
            'fk_departamento',
            'puesto',
        )
        # Usar correo como identificador único para importaciones
        import_id_fields = ('correo',)
        skip_unchanged = True
        report_skipped = True
        use_transactions = True

    def before_import_row(self, row, **kwargs):
        """Procesar datos antes de importar cada fila"""
        print(f"\n=== PROCESANDO EMPLEADO ===")
        print(f"Empleado: '{row.get('nombre_empleado')}'")
        print(f"Correo: '{row.get('correo')}'")
        print(f"Departamento: '{row.get('fk_departamento')}' (tipo: {type(row.get('fk_departamento'))})")
        print(f"Sucursal: '{row.get('fk_sucursal')}' (tipo: {type(row.get('fk_sucursal'))})")

        # Limpiar espacios en blanco y valores vacíos
        for key, value in row.items():
            if isinstance(value, str):
                cleaned_value = value.strip()
                row[key] = cleaned_value if cleaned_value else None
            elif value == '':
                row[key] = None

        # Campos que pueden estar vacíos
        empty_to_none_fields = [
            'nombre_empleado', 'correo', 'fk_sucursal', 'fk_departamento', 'puesto'
        ]

        for field in empty_to_none_fields:
            if row.get(field) in ['', None, 'NULL', 'null', 'N/A', 'n/a']:
                row[field] = None

        # Validación básica de correo
        correo = row.get('correo')
        if correo and '@' not in correo:
            print(f"⚠️ ADVERTENCIA: El correo '{correo}' no parece válido")

        print(f"Departamento procesado: '{row.get('fk_departamento')}'")
        print(f"Sucursal procesada: '{row.get('fk_sucursal')}'")
        print("=== FIN PROCESAMIENTO EMPLEADO ===\n")

    def import_obj(self, obj, data, dry_run):
        """Procesar el objeto antes de guardarlo"""
        print(f"\n--- IMPORT_OBJ EMPLEADO DEBUG ---")
        print(f"Datos recibidos:")
        print(f"  nombre_empleado: {data.get('nombre_empleado')}")
        print(f"  correo: {data.get('correo')}")
        print(f"  puesto: {data.get('puesto')}")
        print(f"  departamento: {data.get('fk_departamento')}")
        print(f"  sucursal: {data.get('fk_sucursal')}")

        # Verificar si los objetos relacionados existen
        if data.get('fk_departamento'):
            try:
                departamento = Departamento.objects.get(nombre=data.get('departamento'))
                print(f"  ✓ Departamento encontrado: {departamento}")
            except Departamento.DoesNotExist:
                print(f"  ✗ Departamento NO encontrado: {data.get('departamento')}")
                print(f"  Departamentos disponibles: {list(Departamento.objects.values_list('nombre', flat=True))}")

        if data.get('sucursal'):
            try:
                sucursal = Sucursal.objects.get(nombre_suc=data.get('sucursal'))
                print(f"  ✓ Sucursal encontrada: {sucursal}")
            except Sucursal.DoesNotExist:
                print(f"  ✗ Sucursal NO encontrada: {data.get('sucursal')}")
                print(f"  Sucursales disponibles: {list(Sucursal.objects.values_list('nombre_suc', flat=True))}")

        print("--- FIN IMPORT_OBJ EMPLEADO DEBUG ---\n")

        return super().import_obj(obj, data, dry_run)

    def after_import_row(self, row, row_result, **kwargs):
        """Procesar después de importar cada fila (para debug)"""
        if row_result.errors:
            print(f"Errores en fila empleado: {row_result.errors}")
        if hasattr(row_result, 'object_repr'):
            print(f"Empleado procesado: {row_result.object_repr}")

    def skip_row(self, instance, original, row, import_validation_errors=None):
        """Decidir si saltar una fila durante la importación"""
        # Saltar si no hay nombre o correo
        if not row.get('nombre_empleado') or not row.get('correo'):
            print(f"⚠️ Saltando fila: falta nombre_empleado o correo")
            return True
        
        return super().skip_row(instance, original, row, import_validation_errors)