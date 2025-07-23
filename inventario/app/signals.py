from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app.models import Equipo, EquipoEliminado

@receiver(pre_delete, sender=Equipo)
def crear_equipo_eliminado(sender, instance, using, **kwargs):
    # Puedes obtener el usuario y motivo desde el contexto si lo necesitas
    EquipoEliminado.crear_desde_equipo(
        equipo_instance=instance,
        usuario=getattr(instance, '_usuario_eliminacion', None),
        motivo=getattr(instance, '_motivo_eliminacion', None)
    )