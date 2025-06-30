#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build process..."


echo "📦 Instalando dependencias..."
pip install -r ../requirements.txt

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "🏗️ Creando datos iniciales..."
python manage.py shell << 'EOF'
# Aquí tu script Python para datos iniciales (igual que ya tienes)
EOF

echo "👤 Creando superusuario..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@boticacentral.com', 'InventarioBC2024!')
    print('✅ Superuser creado: admin / InventarioBC2024!')
else:
    print('ℹ️ Superuser ya existe')
EOF

echo "🎉 Build completado exitosamente!"
