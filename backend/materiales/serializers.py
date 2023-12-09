from rest_framework import serializers
from materiales.models import (
    Ejemplar,
    Material,
    Autor,
    Carrera,
    Editorial,
    Genero,
    TipoMaterial,
)
from reservas.models import Reserva, Prestamo
from accounts.models import User

from .utils import (
    get_cantidad_disponible,
    get_cantidad_en_reserva,
    get_cantidad_existente,
    get_estado,
)


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = "__all__"


class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = "__all__"


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = "__all__"


class TipoMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMaterial
        fields = "__all__"


class EjemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejemplar
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    cantidad_existente = serializers.SerializerMethodField()
    cantidad_en_reserva = serializers.SerializerMethodField()
    cantidad_disponible = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    

    class Meta:
        model = Material
        fields = [
            "id",
            "titulo",
            "descripcion",
            "tipo",
            "editorial",
            "autor",
            "carrera",
            "genero",
            "cantidad_existente",
            "cantidad_en_reserva",
            "cantidad_disponible",
            "estado",
        ]

    def get_cantidad_existente(self, obj):
        return get_cantidad_existente(obj)

    def get_cantidad_en_reserva(self, obj):
        return get_cantidad_en_reserva(obj)

    def get_cantidad_disponible(self, obj):
        return get_cantidad_disponible(obj)

    def get_estado(self, obj):
        return get_estado(obj)
