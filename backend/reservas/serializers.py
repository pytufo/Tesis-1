from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from materiales.serializers import MaterialSerializer
from .models import Reserva, Prestamo


class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            "id",
            "fecha_inicio",
            "fecha_fin",
            "owner",
            "material",
        ]


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = "__all__"
