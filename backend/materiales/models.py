from django.db import models
from django.urls import reverse
from accounts.models import User


class Ejemplar(models.Model):
    # Definimos los estados
    ESTADO = (
        ("d", "Disponible"),
        ("n", "No disponible"),
    )
    # Campos
    articulo = models.ForeignKey(
        "Articulo", on_delete=models.CASCADE, null=False, related_name="reserva"
    )
    estado = models.CharField(
        max_length=1,
        choices=ESTADO,
        blank=True,
        null=True,
        help_text="Estado de Ejemplar",
        default="d"
    )

    class Meta:
        ordering = ["articulo"]

    def __str__(self):
        return "%s" % (self.articulo)

    def get_absolute_url(self):
        return reverse("ejemplar_detail", args=[str(self.id, self.articulo)])


class Articulo(models.Model):
    # Campos
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    tipo = models.ManyToManyField("TipoMaterial", related_name="tipo", blank=True)
    editorial = models.ManyToManyField(
        "Editorial", related_name="editorial", blank=True
    )
    autor = models.ManyToManyField("Autor", related_name="autor", blank=True)
    carrera = models.ManyToManyField("Carrera", related_name="carrera", blank=True)
    genero = models.ManyToManyField("Genero", related_name="genero", blank=True)

    # Metadata
    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("detail_articulo", args=[str(self.id)])


class Editorial(models.Model):
    nombre = models.CharField(max_length=70)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse("editorial-view", args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=70)
    apellido = models.CharField(max_length=100)

    class Meta:
        ordering = ["apellido", "nombre"]

    def get_absolute_url(self):
        return reverse("autor-view", args=[str(self.id)])

    def __str__(self):
        return "%s, %s" % (self.nombre, self.apellido)


class TipoMaterial(models.Model):
    nombre = models.CharField(max_length=70)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse("tipo-material-view", args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Genero(models.Model):
    nombre = models.CharField(max_length=70)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse("genero-view", args=[str(self.id)])

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    nombre = models.CharField(max_length=70)

    class Meta:
        ordering = ["nombre"]

    def get_absolute_url(self):
        return reverse("carrera-view", args=[str(self.id)])

    def __str__(self):
        return self.nombre
