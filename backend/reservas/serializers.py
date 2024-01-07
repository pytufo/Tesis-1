from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reserva, Prestamo, ListaEspera
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


class ReservaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ["fecha_fin", "owner", "material"]
        read_only_fields = ["material", "fecha_fin"]

    def __init__(self, *args, **kwargs):
        material_pk = kwargs.pop("material_pk", None)
        super().__init__(*args, **kwargs)

        if material_pk is not None:
            self.fields["material"].queryset = Material.objects.filter(pk=material_pk)


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


class ListaDeEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaEspera
        fields = ["fecha_fin", "owner", "material"]
        read_only_fields = ["material", "fecha_fin"]


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = [
            "id",
            "fecha_fin",
            "created_by",
            "owner",
            "ejemplar",
        ]
