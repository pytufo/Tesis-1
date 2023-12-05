from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from materiales.models import Ejemplar
from .models import Reserva, Prestamo


@receiver(post_save, sender=Reserva)
@receiver(post_save, sender=Prestamo)


def actualizar_estado_ejemplar(sender, instance, **kwargs):
    ejemeplar = instance.ejemplar
    ejemeplar.estado = Ejemplar.NO_DISPONE


post_save.connect(actualizar_estado_ejemplar, sender=Reserva)
post_save.connect(actualizar_estado_ejemplar, sender=Prestamo)
