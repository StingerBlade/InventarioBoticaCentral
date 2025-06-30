#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build process..."

# Cambiar directorio a donde está manage.py
cd inventario

echo "📦 Instalando dependencias..."
pip install -r ../requirements.txt

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "🏗️ Creando datos iniciales..."
python manage.py shell << 'EOF'
from app.models import Estado, Municipio, RazonSocial, Sucursal, Tipo_Sucursal, TipoEquipo, Disponibilidad, TipoAlmacenamiento, TipoMantenimiento

estados_data = [
    'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas',
    'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 'Durango',
    'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco',
    'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
    'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
    'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz',
    'Yucatán', 'Zacatecas'
]

for estado_nombre in estados_data:
    Estado.objects.get_or_create(nombre_est=estado_nombre)

chihuahua_estado = Estado.objects.get(nombre_est='Chihuahua')
municipios_chihuahua = [
    'Chihuahua', 'Delicias', 'Cuauhtemoc', 'Aldama', 'Camargo', 'Parral', 'Juarez'
]

for municipio_nombre in municipios_chihuahua:
    Municipio.objects.get_or_create(
        nombre_mun=municipio_nombre,
        fk_estado=chihuahua_estado
    )

RazonSocial.objects.get_or_create(razon='Futufarma')
RazonSocial.objects.get_or_create(razon='Futumedical')

Tipo_Sucursal.objects.get_or_create(nombre_tipo_sucursal='Farmacia')
Tipo_Sucursal.objects.get_or_create(nombre_tipo_sucursal='Corporativo')
Tipo_Sucursal.objects.get_or_create(nombre_tipo_sucursal='Planta')

Disponibilidad.objects.get_or_create(nombre='Disponible')
Disponibilidad.objects.get_or_create(nombre='En préstamo')
Disponibilidad.objects.get_or_create(nombre='Asignado')
Disponibilidad.objects.get_or_create(nombre='En reparación')
Disponibilidad.objects.get_or_create(nombre='Fuera de servicio')

tipos_equipo = [
    'Desktop', 'Laptop', 'Impresora', 'Escaner', 'Servidor',
    'Monitor', 'Proyector', 'Router', 'Switch', 'Teléfono IP'
]

for tipo_nombre in tipos_equipo:
    TipoEquipo.objects.get_or_create(nombre_tipo_equipo=tipo_nombre)

tipos_almacenamiento = ['HDD', 'SSD', 'eMMC', 'NVMe']
for tipo_alm in tipos_almacenamiento:
    TipoAlmacenamiento.objects.get_or_create(nombre=tipo_alm)

def crear_tipo(nombre, padre=None):
    obj, created = TipoMantenimiento.objects.get_or_create(nombre=nombre, padre=padre)
    return obj

preventivo = crear_tipo("Preventivo")
correctivo = crear_tipo("Correctivo")

inspeccion = crear_tipo("Inspección", preventivo)
limpieza = crear_tipo("Limpieza", preventivo)
optimizacion = crear_tipo("Optimización", preventivo)

cpu = crear_tipo("CPU", limpieza)
monitor = crear_tipo("Monitor", limpieza)
teclado_mouse = crear_tipo("Teclado/Mouse", limpieza)

reparacion_software = crear_tipo("Reparación de software", correctivo)
reparacion_hardware = crear_tipo("Reparación de hardware", correctivo)

reinstalar_windows = crear_tipo("Reinstalar Windows", reparacion_software)
desinstalacion_programas = crear_tipo("Desinstalación de programas", reparacion_software)

reemplazo_componente = crear_tipo("Reemplazo de componente", reparacion_hardware)

print("✅ Datos iniciales creados correctamente.")
EOF

echo "👤 Creando superusuario..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@boticacentral.com', 'InventarioBC2024!')
    print('✅ Superuser created: admin / InventarioBC2024!')
else:
    print('ℹ️ Superuser already exists')
EOF

echo "🎉 Build completado exitosamente!"
