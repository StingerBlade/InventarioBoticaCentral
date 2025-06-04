from django.db import models
from django.core.exceptions import ValidationError

class Estado(models.Model):
    nombre_est = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_est

class Municipio(models.Model):
    nombre_mun = models.CharField(max_length=100)
    fk_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_mun

class Sucursal(models.Model):
    nombre_suc = models.CharField(max_length=100)
    fk_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_suc

class RazonSocial(models.Model):
    razon = models.CharField(max_length=100)

    def __str__(self):
        return self.razon

class TipoEquipo(models.Model):
    nombre_tipo_equipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_tipo_equipo

class TipoAlmacenamiento(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo de Almacenamiento"
        verbose_name_plural = "Tipos de Almacenamiento"

    def __str__(self):
        return self.nombre

class Disponibilidad(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Estado de Disponibilidad"
        verbose_name_plural = "Estados de Disponibilidad"

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100)
    correo = models.EmailField(null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre_empleado

class Equipo(models.Model):
    tipo = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True)
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True)
    tipo_almacenamiento = models.ForeignKey(TipoAlmacenamiento, on_delete=models.SET_NULL, null=True)
    capacidad_almacenamiento = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    procesador = models.CharField(max_length=100, null=True, blank=True)
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.marca} {self.modelo}"

class Mantenimiento(models.Model):
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha = models.DateField()
    diagnostico = models.CharField(max_length=255)
    solucion = models.CharField(max_length=255)
    tecnico = models.CharField(max_length=100)
    estatus = models.CharField(max_length=50, default='Pendiente')

    def __str__(self):
        return f"Mantenimiento de {self.fk_equipo} en {self.fecha}"

class Prestamo(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.fk_equipo.disponibilidad.nombre != 'Disponible':
            raise ValidationError("Este equipo no está disponible para préstamo.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean()
        super().save(*args, **kwargs)
        # Cambiar disponibilidad del equipo
        en_prestamo = Disponibilidad.objects.get(nombre='En préstamo')
        self.fk_equipo.disponibilidad = en_prestamo
        self.fk_equipo.save()

    def __str__(self):
        return f"Préstamo de {self.fk_equipo} a {self.fk_empleado}"

class DispositivoMovil(models.Model):
    PLAN_CHOICES = [
        ('Plan', 'Plan'),
        ('Prepago', 'Prepago'),
    ]
    imei = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_celular = models.CharField(max_length=20)
    tipo_plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_celular}"
