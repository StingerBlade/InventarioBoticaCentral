# proyectoEstadias
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/StingerBlade/proyectoEstadias)

Sistema de Inventario

# 📦 Inventario Botica Central

## Descripción general

**Inventario Botica Central** es un sistema de gestión de inventario desarrollado en Django, diseñado para realizar el seguimiento de equipos de TI, la administración de personal y la programación de mantenimiento en múltiples sucursales farmacéuticas en México. Proporciona una gestión centralizada de activos, registros de empleados y operaciones de mantenimiento para organizaciones que operan bajo distintas razones sociales.

---

## ✨ Características

* Gestión de **Equipos**, **Empleados**, **Préstamos** y **Asignaciones** mediante modelos de Django.
* Registro de **mantenimientos** con soporte para jerarquía de tipos de mantenimiento.
* Administración de entidades geográficas: **Estados**, **Municipios**, **Sucursales**, **Razón Social** y **Departamentos**.
* Importación y exportación de datos en formatos Excel/CSV con `django-import-export`.
* Gestión de archivos estáticos en producción con **WhiteNoise**.
* Despliegue flexible con configuración basada en variables de entorno.
* Soporte para desarrollo local con SQLite y producción en PostgreSQL (local o Supabase).

---

## 🧱 Estructura del proyecto

```
inventario/
├── inventario/      # Configuración principal del proyecto
│   ├── settings.py  # Configuración de apps, DB, seguridad, import/export, static, entorno
│   ├── urls.py      # Rutas globales
│   └── …
├── app/             # Módulo principal de negocio
│   ├── models.py    # Modelos: Estado, Municipio, Sucursal, RazonSocial, TipoMantenimiento, Equipo, Empleado, etc.
│   ├── views.py     # Lógica de negocio
│   ├── admin.py     # Administración: EquipoAdmin, EmpleadoAdmin
│   ├── resources.py # Recursos para import/export (EquipoResource)
│   ├── urls.py      # Rutas específicas de la app
│   ├── templates/   # Plantillas HTML
│   └── static/      # CSS, imágenes
└── manage.py
```

---

## ⚙️ Dependencias y stack tecnológico

| Componente              | Tecnología            | Objetivo                            |
| ----------------------- | --------------------- | ----------------------------------- |
| Framework web           | Django 5.2.1          | Base del proyecto                   |
| Base de datos           | PostgreSQL / Supabase | Almacenamiento principal            |
| Importación/Exportación | django-import-export  | Procesamiento de archivos Excel/CSV |
| Archivos estáticos      | WhiteNoise            | Servicio en producción              |
| Variables de entorno    | python-dotenv         | Gestión de configuración segura     |
| Despliegue              | Render.com            | Hosting para producción             |

---

## 🔧 Variables de entorno

Configura un archivo `.env` en la raíz con:

```dotenv
SECRET_KEY=tu_clave_secreta
DEBUG=True  # o False en producción
DATABASE_URL=postgres://...  # para producción
RENDER_EXTERNAL_HOSTNAME=tu_app.render.com  # sólo en deploy
DB_NAME=inventario  # opcional, para desarrollo local
```

---

## 🚀 Instalación local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/StingerBlade/InventarioBoticaCentral.git
   cd InventarioBoticaCentral
   ```
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # en Windows: venv\Scripts\activate
   ```
3. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Crea el archivo `.env` como se describió arriba.
5. Ejecuta migraciones:

   ```bash
   python manage.py migrate
   ```
6. Inicializa datos base en Django shell (Estados, Municipios, Razón Social…):

   ```bash
   python manage.py shell
   >>> from app.models import TipoMantenimiento
   >>> # Crea jerarquía de tipos de mantenimiento
   ```
7. Arranca el servidor local:

   ```bash
   python manage.py runserver
   ```

---

## 📦 Uso en producción

1. Asegúrate de definir en `.env`:

   * `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `RENDER_EXTERNAL_HOSTNAME`.
2. Habilita `WhiteNoise` y configuraciones de seguridad (SSL, HSTS, cookies seguras).
3. Ejecuta `collectstatic`:

   ```bash
   python manage.py collectstatic
   ```
4. Despliega en **Render.com** o plataforma similar.
5. Administra datos a través del panel de Django Admin.

---

## 📈 Procesos de importación/exportación

El sistema permite gestionar datos de equipos mediante archivos `.xlsx` o `.csv` desde Django Admin, usando `EquipoResource` en `app/resources.py`. Las importaciones usan transacciones para mayor integridad, manteniendo un registro de operaciones y resolviendo claves foráneas automáticamente.

---

