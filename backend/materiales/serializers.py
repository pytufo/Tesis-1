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


""" class ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "role"]
 """


class EjemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejemplar
        fields = "__all__"


class ArticuloSerializer(serializers.ModelSerializer):
    # ejemplar = EjemplarSerializer(write_only=True)

    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "descripcion",
            "tipo",
            "editorial",
            "autor",
            "carrera",
            "genero",            
        ]


"""
    def create(self, validated_data):
        ejemplar_data = validated_data.pop("ejemplar", None)
        titulo = validated_data.get("titulo")
        articulo_existente = Articulo.objects.filter(titulo=titulo).first()

        if articulo_existente:
            articulo = articulo_existente
        else:
            articulo = Articulo.objects.create(**validated_data)

        if ejemplar_data:
            Ejemplar.objects.create(articulo=articulo, **ejemplar_data)
 """
