from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reserva, Prestamo, ListaEspera
from materiales.serializers import EjemplarSerializer
from materiales.utils import get_ejemplares_de_material

from materiales.models import Material, Ejemplar
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


class MaterialEjemplaresSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(many=True, read_only=True)
    class Meta:
        model = EjemplarSerializer
        fields = ["id", "material"]


class ReservaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ["id", "fecha_fin", "owner", "material"]
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


class EntregaEjemplarReserva(serializers.ModelSerializer):
    # ejemplar = serializers.PrimaryKeyRelatedField(queryset=Ejemplar.objects.none())
    
    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar"]
        

        


class PrestamoCreateSerializer(serializers.ModelSerializer):
    # ejemplar = serializers.PrimaryKeyRelatedField(queryset=Ejemplar.objects.none())

    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar"]

    def __init__(self, *args, **kwargs):
        ejemplar_pk = kwargs.pop("ejemplar_pk", None)
        super().__init__(*args, **kwargs)

        if ejemplar_pk is not None:
            self.fields["ejemplar"].queryset = Ejemplar.objects.filter(pk=ejemplar_pk)
