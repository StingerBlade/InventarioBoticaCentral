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

7. Insertar Estados en la base de datos:
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
8. Insertar municipios con la fk de estado respectivo
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


9. Inserta las razones sociales
    ```bash
    INSERT INTO app_razonsocial (id, razon, correo, direccion, rfc) VALUES
      (1, 'Futufarma', NULL, NULL, NULL),
      (2, 'Futumedical', NULL, NULL, NULL);
    ```
10. Inserta las sucursales
    ```bash
       INSERT INTO app_sucursal (id, nombre_suc, fk_municipio_id, fk_tipo_sucursal_id, fk_razon_social_id) VALUES
      (1, 'Matriz', 1, 1, 1),
      (2, 'Alamedas', 1, 1, 1),
      (3, 'Aldama', 5, 1, 1),
      (4, 'Americas', 1, 1, 1),
      (5, 'Angeles', 1, 1, 1),
      (6, 'Cantera', 1, 1, 1),
      (7, 'CH-P', 1, 1, 1),
      (8, 'Colon', 1, 1, 1),
      (9, 'Comandancia Norte', 1, 1, 1),
      (10, 'Comandancia Sur', 1, 1, 1),
      (11, 'Corporativo Futumedica', 1, 2, 2),
      (12, 'Cuauhtemoc', 3, 1, 1),
      (13, 'Delicias', 2, 1, 1),
      (14, 'Delicias 2', 2, 1, 1),
      (15, 'Ford Corporativo', 10, NULL, NULL),
      (16, 'Ford Mexico', 3, 3, 2),
      (17, 'Ford Hermosillo', 4, 3, 2),
      (18, 'Gas Parral', 7, 1, 1),
      (19, 'Gomez Morin', 2, 1, 1),
      (20, 'IMPE', 1, 1, 1),
      (21, 'Independencia', 7, 1, 1),
      (22, 'JM Iglesias', 1, 1, 1),
      (23, 'Huerta', 3, 1, 1),
      (24, 'Lopez Mateos', 9, 1, 1),
      (25, 'Mirador', 1, 1, 1),
      (26, 'Pensiones', 1, 1, 1),
      (27, 'Politecnico', 1, 1, 1),
      (28, 'UACJ', 9, 1, 1),
      (29, 'Allende', 3, 1, 1),
      (30, 'Morelos', 3, 1, 1),
      (31, 'Zarco', 1, 1, 1),
      (32, 'Aldama', 5, 1, 1),
      (33, 'Camarago', 6, 1, 1),
      (34, 'Cuauhtemoc', 3, 1, 1),
      (35, 'Reliz II', 1, 1, 1),
      (36, 'Bajio', 11, 3, 2),
      (37, 'Mexicali', 13, 3, 2),
      (38, 'Reynosa', 8, 3, 2),
      (39, 'SLP', 14, 3, 2),
      (40, 'Sonora', 4, 3, 2),
      (41, 'Tijuana', 15, 3, 2),
      (42, 'Torreon', 12, 3, 2),
      (43, 'Corporativo Futufarma', 1, 2, 1);
      ```
## Uso

Sigue las instrucciones de la interfaz para añadir, modificar o eliminar productos del inventario.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, por favor crea un pull request o abre un issue.


   

   
