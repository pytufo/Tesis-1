from .models import User
from materiales.models import Material, Ejemplar
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from materiales.utils import (
    get_reservas_prestamos_usuario,
    get_limite_reservas_prestamo,
)
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileSerializer(serializers.ModelSerializer):
    cantidad_reservas = serializers.SerializerMethodField()
    cantidad_prestamos = serializers.SerializerMethodField()
    limite = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "cantidad_reservas",
            "cantidad_prestamos",
            "limite",
        ]

    def get_cantidad_reservas(self, obj):
        return get_reservas_prestamos_usuario(obj)[0]

    def get_cantidad_prestamos(self, obj):
        return get_reservas_prestamos_usuario(obj)[1]

    def get_limite(self, obj):
        return get_limite_reservas_prestamo(obj)


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
        user = authenticate(
            username=data["email"],
            password=data["password"],
        )

        if user is None:
            raise serializers.ValidationError("Usuario o contraseña invalidos")

        """ if user.is_active is False:
            raise serializers.ValidationError("Usuario no habilitado ") """
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                "user": user,
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "role": user.role,
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
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create(email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()

        return user
