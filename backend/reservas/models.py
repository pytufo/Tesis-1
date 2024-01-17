from django.utils import timezone
from django.db import models

# from django.core.exceptions import ValidationError


from accounts.models import User
from materiales.models import Ejemplar, Material

# from materiales.utils import get_cantidad_disponible


from django.urls import reverse


class Reserva(models.Model):
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=False, blank=True, null=True)
    owner = models.ForeignKey(User, related_name="usuario", on_delete=models.CASCADE)
    material = models.ForeignKey(
        Material, related_name="material", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("reservas-view", args=[str(self.id)])

    def __str__(self):
        return str(self.material.titulo)

    class Meta:
        ordering = ["fecha_fin"]



class Prestamo(models.Model):
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=False, blank=True, null=True)
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


class ListaEspera(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Lista de espera para {self.material} - {self.usuario}"

