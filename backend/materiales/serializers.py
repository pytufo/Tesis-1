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


from reservas.utils import get_cantidad_en_espera, get_limite_epera
from .utils import (
    get_cantidad_disponible,
    get_cantidad_en_reserva,
    get_cantidad_en_prestamo,
    get_cantidad_existente,
    get_estado,
    get_estado_ejemplar,
    
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
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Ejemplar
        fields = ["id", "material", "estado"]

    def get_estado(self, obj):
        return get_estado_ejemplar(obj)


class EjemplarMaterialSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Ejemplar
        fields = ["id", "estado"]

    def get_estado(self, obj):
        return get_estado_ejemplar(obj)


class MaterialSerializer(serializers.ModelSerializer):
    cantidad_existente = serializers.SerializerMethodField()
    cantidad_en_reserva = serializers.SerializerMethodField()
    cantidad_en_prestamo = serializers.SerializerMethodField()
    cantidad_en_espera = serializers.SerializerMethodField()
    cantidad_disponible = serializers.SerializerMethodField()
    limite_espera = serializers.SerializerMethodField()
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
            "cantidad_en_prestamo",
            "cantidad_en_espera",
            "cantidad_disponible",
            "limite_espera",
            "estado",            
        ]


    def get_cantidad_existente(self, obj):
        return get_cantidad_existente(obj)

    def get_cantidad_en_reserva(self, obj):
        return get_cantidad_en_reserva(obj)

    def get_cantidad_en_prestamo(self, obj):
        return get_cantidad_en_prestamo(obj)

    def get_cantidad_en_espera(self, obj):
        return get_cantidad_en_espera(obj)

    def get_cantidad_disponible(self, obj):
        return get_cantidad_disponible(obj)

    def get_estado(self, obj):
        return get_estado(obj)

    def get_limite_espera(self, obj):
        return get_limite_epera(obj)
