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
from accounts.serializers import ProfileSerializer
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


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = "__all__"
        read_only_fields = ["cant_d"]


class ListArticuloSerializer(serializers.ModelSerializer):
    tipo = TipoMaterialSerializer(many=True)
    editorial = EditorialSerializer(many=True)
    autor = AutorSerializer(many=True)
    carrera = CarreraSerializer(many=True)
    genero = GeneroSerializer(many=True)

    """self_queryset = Ejemplar.objects.annotate(cant_ejemplares=Sum(Ejemplar))
    print(self_queryset)
     """

    class Meta:
        model = Articulo
        fields = (
            "id",
            "titulo",
            "descripcion",
            "tipo",
            "editorial",
            "carrera",
            "genero",
            "autor",
        )


class ArticuloNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ["id", "titulo"]


class ListEjemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejemplar
        fields = ("id", "articulo", "estado")


class EjemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejemplar
        fields = ("id", "articulo", "estado")


class EjemplarArticuloSerializer(serializers.ModelSerializer):
    articulo = ArticuloNameSerializer()

    class Meta:
        model = Ejemplar
        fields = ["id", "articulo", "estado"]
        read_only_fields = ["estado"]


class ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "role"]
