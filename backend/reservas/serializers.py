from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reserva, Prestamo
from materiales.models import Material
from accounts.models import User

# from materiales.serializers import MaterialSerializer
# from accounts.serializers import UserProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["id", "titulo"]


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
