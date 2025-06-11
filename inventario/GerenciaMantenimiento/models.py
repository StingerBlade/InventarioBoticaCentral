from django.db import models

# Create your models here.


class Aires(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=100)
    fecha_instalacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, choices=[
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('fuera_servicio', 'Fuera de Servicio')
    ], default='operativo')
    ultima_revision = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Aire'
        verbose_name_plural = 'Aires'