# proyectoEstadias
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/StingerBlade/proyectoEstadias)

Sistema de Inventario

## Descripción

Este proyecto es una aplicación para gestionar inventarios, desarrollada principalmente en Python, con componentes en HTML y CSS para la interfaz de usuario. Permite registrar, actualizar y consultar productos, facilitando el control eficiente de los recursos.

## Características

- Registro de productos
- Actualización y eliminación de inventario
- Consulta de stock disponible
- Interfaz de usuario amigable

## Tecnologías utilizadas

- Python
- HTML
- CSS

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/StingerBlade/proyectoEstadias.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd proyectoEstadias
   ```
3. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```
4. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
   **O bien, asegúrate de tener los siguientes paquetes instalados en tu entorno:**
   ```
   asgiref              3.8.1
   diff-match-patch     20241021
   Django               5.2.1
   django-import-export 4.3.7
   et_xmlfile           2.0.0
   mysqlclient          2.2.7
   npm                  0.1.1
   openpyxl             3.1.5
   optional-django      0.1.0
   pip                  25.0.1
   sqlparse             0.5.3
   tablib               3.8.0
   tzdata               2025.2
   ```

## Despliegue

Sigue estos pasos para poner en marcha el proyecto:

5. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```

6. Crea los tipos de mantenimiento en la base de datos:

   Inicia el shell de Django:
   ```bash
   python manage.py shell
   ```

   Copia y ejecuta el siguiente código en el shell para poblar la tabla `TipoMantenimiento`:
   ```python
   from inventario.models import TipoMantenimiento

   # Helper para crear jerárquicamente
   def crear_tipo(nombre, padre=None):
       obj, created = TipoMantenimiento.objects.get_or_create(nombre=nombre, padre=padre)
       return obj

   # Nivel 1
   preventivo = crear_tipo("Preventivo")
   correctivo = crear_tipo("Correctivo")

   # Nivel 2 Preventivo
   inspeccion = crear_tipo("Inspección", preventivo)
   limpieza = crear_tipo("Limpieza", preventivo)
   optimizacion = crear_tipo("Optimización", preventivo)

   # Nivel 3 Limpieza
   cpu = crear_tipo("CPU", limpieza)
   monitor = crear_tipo("Monitor", limpieza)
   teclado_mouse = crear_tipo("Teclado/Mouse", limpieza)

   # Nivel 2 Correctivo
   reparacion_software = crear_tipo("Reparación de software", correctivo)
   reparacion_hardware = crear_tipo("Reparación de hardware", correctivo)

   # Nivel 3 Reparación de software
   reinstalar_windows = crear_tipo("Reinstalar Windows", reparacion_software)
   desinstalacion_programas = crear_tipo("Desinstalación de programas", reparacion_software)

   # Nivel 3 Reparación de hardware
   reemplazo_componente = crear_tipo("Reemplazo de componente", reparacion_hardware)

   print("Tipos de mantenimiento creados correctamente.")
   ```

7. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
   > **¡Importante!** Este servidor es solo para desarrollo. Para producción, usa un servidor WSGI o ASGI profesional. Más información: [Django Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)

## Uso

Sigue las instrucciones de la interfaz para añadir, modificar o eliminar productos del inventario.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, por favor crea un pull request o abre un issue.

8. Insertar Estados en la base de datos:
   ``` bash
   INSERT INTO app_estado  (nombre_est) VALUES 
   ('Aguascalientes'),
   ('Baja California'),
   ('Baja California Sur'),
   ('Campeche'),
   ('Chiapas'),
   ('Chihuahua'),
   ('Ciudad de México'),
   ('Coahuila'),
   ('Colima'),
   ('Durango'),
   ('Estado de México'),
   ('Guanajuato'),
   ('Guerrero'),
   ('Hidalgo'),
   ('Jalisco'),
   ('Michoacán'),
   ('Morelos'),
   ('Nayarit'),
   ('Nuevo León'),
   ('Oaxaca'),
   ('Puebla'),
   ('Querétaro'),
   ('Quintana Roo'),
   ('San Luis Potosí'),
   ('Sinaloa'),
   ('Sonora'),
   ('Tabasco'),
   ('Tamaulipas'),
   ('Tlaxcala'),
   ('Veracruz'),
   ('Yucatán'),
   ('Zacatecas');
   ```
9. Insertar municipios con la fk de estado respectivo
   ```bash
   INSERT INTO app_municipio (id, nombre_mun, fk_estado_id) VALUES
   (1, 'Chihuahua', 6),
   (2, 'Delicias', 6),
   (3, 'Cuauhtemoc', 6),
   (4, 'Hermosillo', 26),
   (5, 'Aldama', 6),
   (6, 'Camargo', 6),
   (7, 'Parral', 6),
   (8, 'Reynosa', 28),
   (9, 'Juarez', 6),
   (10, 'Naucalpan de Juarez', 15),
   (11, 'Leon', 12),
   (12, 'Torreon', 10),
   (13, 'Mexicali', 2),
   (14, 'San Luis Potosi', 24),
   (15, 'Tijuana', 2);
   ```

   

   
