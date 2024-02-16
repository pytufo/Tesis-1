from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reserva, Prestamo, ListaEspera

from materiales.utils import get_ejemplares_de_material

from materiales.models import Material, Ejemplar
from materiales.serializers import MaterialSerializer, EjemplarSerializer
from accounts.models import User
from accounts.serializers import UserProfileSerializer

# from materiales.serializers import MaterialSerializer
# from accounts.serializers import UserProfileSerializer



class ReservaCreateSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    material = MaterialSerializer()
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
    owner = UserProfileSerializer()
    ejemplar = EjemplarSerializer()
    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar"]

    def __init__(self, *args, **kwargs):
        ejemplar_pk = kwargs.pop("ejemplar_pk", None)
        super().__init__(*args, **kwargs)

        if ejemplar_pk is not None:
            self.fields["ejemplar"].queryset = Ejemplar.objects.filter(pk=ejemplar_pk)
