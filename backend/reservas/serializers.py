from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Reserva, Prestamo

from materiales.utils import get_ejemplares_de_material
from .utils import get_estado_prestamo, get_estado_reserva
from materiales.models import Material, Ejemplar
from materiales.serializers import MaterialSerializer, EjemplarSerializer
from accounts.models import User
from accounts.serializers import UserProfileSerializer

# from materiales.serializers import MaterialSerializer
# from accounts.serializers import UserProfileSerializer


class ReservaCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all())
    fecha_fin = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Reserva
        fields = ["id", "fecha_fin", "owner", "material"]
        read_only_fields = ["material"]

    def __init__(self, *args, **kwargs):
        material_pk = kwargs.pop("material_pk", None)
        super().__init__(*args, **kwargs)

        if material_pk is not None:
            self.fields["material"].queryset = Material.objects.filter(pk=material_pk)


class ReservasSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()
    owner = UserProfileSerializer()
    estado = serializers.SerializerMethodField()
    fecha_fin = serializers.DateTimeField()

    class Meta:
        model = Reserva
        fields = ["id", "fecha_fin", "owner", "material", "estado"]
        ordering = ["-fecha_fin"]

    def get_estado(self, obj):
        return get_estado_reserva(obj)


class PrestamosSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    created_by = UserProfileSerializer()
    ejemplar = EjemplarSerializer()
    estado = serializers.SerializerMethodField()
    fecha_fin = serializers.DateTimeField()

    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar", "estado"]
        ordering = ["-fecha_fin"]

    def get_estado(self, obj):
        return get_estado_prestamo(obj)


class EntregaEjemplarReserva(serializers.ModelSerializer):
    # ejemplar = serializers.PrimaryKeyRelatedField(queryset=Ejemplar.objects.none())

    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar"]


class PrestamoCreateSerializer(serializers.ModelSerializer):
    # ejemplar = serializers.PrimaryKeyRelatedField(queryset=Ejemplar.objects.none())
    fecha_fin = serializers.DateTimeField()

    class Meta:
        model = Prestamo
        fields = ["id", "fecha_fin", "created_by", "owner", "ejemplar"]
        ordering = ["-fecha_fin"]

    def __init__(self, *args, **kwargs):
        ejemplar_pk = kwargs.pop("ejemplar_pk", None)
        super().__init__(*args, **kwargs)

        if ejemplar_pk is not None:
            self.fields["ejemplar"].queryset = Ejemplar.objects.filter(pk=ejemplar_pk)
