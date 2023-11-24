from rest_framework import serializers

from materiales.serializers import ownerSerializer
from .models import Reservas, Prestamos, Ejemplar


class CreateReservaserializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = ["fecha_fin", "owner", "articulo"]
        read_only_fields = ["owner"]


class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejemplar
        fields = ["id", "articulo", "estado"]


class ListReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = ("fecha_fin", "owner", "articulo")


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamos
        fields = "__all__"
