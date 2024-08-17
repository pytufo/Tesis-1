from .models import User
from materiales.models import Material, Ejemplar
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from reservas.utils import (
    get_reservas_prestamos_usuario,
    get_limite_reservas_prestamo,
)

from facturacion.utils import (
    es_moroso,
    total_cuotas_atrasadas
)
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileSerializer(serializers.ModelSerializer):
    usuario_reservas = serializers.SerializerMethodField()
    cantidad_reservas = serializers.SerializerMethodField()
    usuario_prestamos = serializers.SerializerMethodField()
    cantidad_prestamos = serializers.SerializerMethodField()
    limite = serializers.SerializerMethodField()
    role = serializers.CharField(source="get_role_display", read_only=False)

    morosidad = serializers.SerializerMethodField()
    cuotas_atrasadas = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "dni",
            "username",
            "first_name",
            "last_name",
            "email",
            "cantidad_reservas",
            "usuario_reservas",
            "cantidad_prestamos",
            "usuario_prestamos",
            "limite",
            "is_active",
            "is_authenticated",
            "morosidad",
            "cuotas_atrasadas",
            "role",
        ]

    def get_cantidad_reservas(self, obj):
        return get_reservas_prestamos_usuario(obj)["cantidad_reservas"]

    def get_cantidad_prestamos(self, obj):
        return get_reservas_prestamos_usuario(obj)["cantidad_prestamos"]

    def get_usuario_reservas(self, obj):
        return get_reservas_prestamos_usuario(obj)["reservas_usuario"]

    def get_usuario_prestamos(self, obj):
        return get_reservas_prestamos_usuario(obj)["prestamos_usuario"]

    def get_limite(self, obj):
        return get_limite_reservas_prestamo(obj)
    
    def get_morosidad(self,obj):
        return es_moroso(obj)
    
    def get_cuotas_atrasadas(self, obj):
        return total_cuotas_atrasadas(obj)


""" 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
 """


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        owner = authenticate(
            username=data["email"],
            password=data["password"],
        )

        if owner is None:
            error_message = "Usuario o contraseña invalidos"
            raise serializers.ValidationError(error_message)

        """ if user.is_active is False:
            raise serializers.ValidationError("Usuario no habilitado ") """
        try:
            refresh = RefreshToken.for_user(owner)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                "owner": owner,
                "access": access_token,
                "refresh": refresh_token,
                "id": owner.id,
                "email": owner.email,
                "role": owner.role,
                "reservas": serializers.PrimaryKeyRelatedField(
                    many=True, queryset=Material.objects.all()
                ),
                "en propiedad": serializers.PrimaryKeyRelatedField(
                    many=True, queryset=Ejemplar.objects.all()
                ),
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("email", "password", "dni", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            dni=validated_data["dni"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
