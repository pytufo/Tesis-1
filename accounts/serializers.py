from .models import User
from materiales.models import Articulo, Ejemplar
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','password', 'email', 'role']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

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
        user = authenticate(username=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError("Usuario o contraseña invalidos")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
                'reservas': serializers.PrimaryKeyRelatedField(many=True, queryset=Articulo.objects.all()),
                'en propiedad': serializers.PrimaryKeyRelatedField(many=True, queryset=Ejemplar.objects.all())
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
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], email=validated_data['email'])

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )
