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
from reservas.utils import get_estado_prestamo, get_estado_reserva

# from reservas.serializers import ReservasSerializer, PrestamosSerializer


from reservas.utils import get_limite_epera, get_reservas_prestamos_usuario
from .utils import (
    get_cantidad_disponible,
    get_cantidad_en_reserva,
    get_cantidad_en_prestamo,
    get_cantidad_existente,
    get_estado,
    get_estado_ejemplar,
    get_ejemplares_disponibles,
    get_carreras_de_material,
    get_autores_de_material,
    get_editoriales_de_material,
    get_generos_de_material,
    get_tipos_de_material,
)


class AutorSerializer(serializers.ModelSerializer):
    cant_materiales = serializers.SerializerMethodField()

    class Meta:
        model = Autor
        fields = ["id", "nombre", "apellido", "cant_materiales"]

    def get_cant_materiales(self, obj):
        return get_autores_de_material(obj).count()


class CarreraSerializer(serializers.ModelSerializer):
    cant_materiales = serializers.SerializerMethodField()

    class Meta:
        model = Carrera
        fields = ["id", "nombre", "cant_materiales"]

    def get_cant_materiales(self, obj):
        return get_carreras_de_material(obj).count()


class EditorialSerializer(serializers.ModelSerializer):
    cant_materiales = serializers.SerializerMethodField()

    class Meta:
        model = Editorial
        fields = ["id", "nombre", "cant_materiales"]

    def get_cant_materiales(self, obj):
        return get_editoriales_de_material(obj).count()


class GeneroSerializer(serializers.ModelSerializer):
    cant_materiales = serializers.SerializerMethodField()

    class Meta:
        model = Genero
        fields = ["id", "nombre", "cant_materiales"]

    def get_cant_materiales(self, obj):
        return get_generos_de_material(obj).count()


class TipoMaterialSerializer(serializers.ModelSerializer):
    cant_materiales = serializers.SerializerMethodField()

    class Meta:
        model = TipoMaterial
        fields = ["id", "nombre", "cant_materiales"]

    def get_cant_materiales(self, obj):
        return get_tipos_de_material(obj).count()


class EjemplarMaterialSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Ejemplar
        fields = ["id", "estado"]

    def get_estado(self, obj):
        return get_estado_ejemplar(obj)


class ReservaSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    class Meta:
        model = Reserva
        fields = ["id", "fecha_inicio", "fecha_fin", "owner", "visto", "estado"]

    def get_estado(self, obj):
        return get_estado_reserva(obj)


class PrestamoSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    class Meta:
        model = Prestamo
        fields = ["id", "fecha_inicio", "fecha_fin", "owner", "visto", "estado"]

    def get_estado(self,obj):
        return get_estado_prestamo(obj)


class MaterialSerializer(serializers.ModelSerializer):
    cantidad_existente = serializers.SerializerMethodField()
    cantidad_en_reserva = serializers.SerializerMethodField()
    cantidad_en_prestamo = serializers.SerializerMethodField()
    cantidad_disponible = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    ejemplares_disponibles = serializers.SerializerMethodField()

    reserva = serializers.SerializerMethodField()
    prestamo = serializers.SerializerMethodField()

    # Ya que por defecto los subcampos de material serian indices, convertimos estos en cadenas de texto correspondiente a cada campo
    tipo = TipoMaterialSerializer(many=True, read_only=True)
    editorial = EditorialSerializer(many=True, read_only=True)
    autor = AutorSerializer(many=True, read_only=True)
    carrera = CarreraSerializer(many=True, read_only=True)
    genero = GeneroSerializer(many=True, read_only=True)

    ##Añadir movimientos del material
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
            "cantidad_disponible",
            "estado",
            "ejemplares_disponibles",
            "reserva",
            "prestamo",
        ]

    def get_reserva(self, obj):
        reserva = Reserva.objects.filter(material=obj).order_by("-fecha_inicio").first()
        if reserva:
            return ReservaSerializer(reserva).data
        return None

    def get_prestamo(self, obj):
        prestamo = (
            Prestamo.objects.filter(ejemplar__material=obj)
            .order_by("-fecha_inicio")
            .first()
        )
        if prestamo:
            return PrestamoSerializer(prestamo).data
        return None

    def get_cantidad_existente(self, obj):
        return get_cantidad_existente(obj)

    def get_cantidad_en_reserva(self, obj):
        return get_cantidad_en_reserva(obj)

    def get_cantidad_en_prestamo(self, obj):
        return get_cantidad_en_prestamo(obj)

    def get_cantidad_disponible(self, obj):
        return get_cantidad_disponible(obj)

    def get_estado(self, obj):
        return get_estado(obj)

    def get_limite_espera(self, obj):
        return get_limite_epera(obj)

    def get_ejemplares_disponibles(self, obj):
        return get_ejemplares_disponibles(obj)


class EjemplarSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Ejemplar
        fields = [
            "id",
            "estado",
            "material",
        ]

    def get_estado(self, obj):
        return get_estado_ejemplar(obj)
