from django.db import models

# from django.core.exceptions import ValidationError


from accounts.models import User
from materiales.models import Ejemplar, Articulo

# from materiales.utils import get_cantidad_disponible


from django.urls import reverse


class Reserva(models.Model):
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=False)
    owner = models.ForeignKey(User, related_name="usuario", on_delete=models.CASCADE)
    articulo = models.ForeignKey(
        Articulo, related_name="articulo", on_delete=models.CASCADE
    )

    """ def save(self, *args, **kwargs):
        cantidad_disponible = get_cantidad_disponible(self.articulo)

        if cantidad_disponible < 1:
            raise ValidationError("No hay ejemplares disponibles para la reserva.")

        super().save(*args, **kwargs) """

    def get_absolute_url(self):
        return reverse("reservas-view", args=[str(self.id)])

    def __str__(self):
        return str(self.articulo.titulo)

    class Meta:
        ordering = ["fecha_fin"]


class Prestamo(models.Model):
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=False)
    created_by = models.ForeignKey(User, related_name="Autor", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="Prestamos", on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(
        Ejemplar, related_name="ejemplar", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("prestamos-view", args=[str(self.id)])

    def __str__(self):
        return f"Prestamo de {self.ejemplar}  ({self.fecha_inicio} - {self.fecha_fin})"

    class Meta:
        ordering = ["fecha_fin"]
