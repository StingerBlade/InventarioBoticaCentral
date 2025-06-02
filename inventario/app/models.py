from django.db import models

# Create your models here.

class Estado(models.Model):
    nombre_est = models.CharField(max_length=100)

class Municipio(models.Model):
    nombre_mun = models.CharField(max_length=100)
    fk_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Sucursal(models.Model):
    nombre_suc = models.CharField(max_length=100)
    fk_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

class RazonSocial(models.Model):
    razon = models.CharField(max_length=100)

class TipoEquipo(models.Model):
    nombre_tipo_equipo = models.CharField(max_length=50)

class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100)
    correo = models.EmailField(null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)

class Equipo(models.Model):
    tipo = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=20, default='Disponible')
    descripcion = models.TextField(null=True, blank=True)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    almacenamiento = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    procesador = models.CharField(max_length=100, null=True, blank=True)
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True)

class Mantenimiento(models.Model):
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateField()
    diagnostico = models.CharField(max_length=255)
    solucion = models.CharField(max_length=255)
    tecnico = models.CharField(max_length=100)
    estatus = models.CharField(max_length=50, default='Pendiente')

class Prestamo(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True)

class DispositivoMovil(models.Model):
    PLAN_CHOICES = [
        ('Datos', 'Datos'),
        ('Prepago', 'Prepago'),
    ]
    imei = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_celular = models.CharField(max_length=20)
    tipo_plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)


class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    passwd = models.CharField(max_length=255)  # Aquí se guarda el hash

    def __str__(self):
        return self.nombre