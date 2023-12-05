from rest_framework import serializers
from materiales.models import (
    Ejemplar,
    Articulo,
    Autor,
    Carrera,
    Editorial,
    Genero,
    TipoMaterial,
)
from accounts.models import User


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


class ArticuloSerializer(serializers.ModelSerializer):
    cantidad_existente = serializers.SerializerMethodField()

    class Meta:
        model = Articulo
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
        ]

    def get_cantidad_existente(self, obj):
        return Ejemplar.objects.filter(articulo=obj.id).count()
