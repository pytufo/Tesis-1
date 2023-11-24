from django.db import models
from accounts.models import User
from materiales.models import Articulo, Ejemplar
from django.urls import reverse


class Reserva(models.Model):
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=False)
    owner = models.ForeignKey(User, related_name="Reservas", on_delete=models.CASCADE)
    articulo = models.ForeignKey(
        Articulo, related_name="articulo", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("reservas-view", args=[str(self.id)])

    def __str__(self):
        return self.articulo.titulo

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
        return f"Prestamo de {self.ejemplar} ({self.fecha_inicio} - {self.fecha_fin})"

    class Meta:
        ordering = ["fecha_fin"]
