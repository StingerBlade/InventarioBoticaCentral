#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build process..."

echo "📦 Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "✅ Base de datos ya configurada, omitiendo inicialización de datos..."

echo "✅ Superusuario ya configurado, omitiendo creación..."

echo "🎉 Build completado exitosamente!"