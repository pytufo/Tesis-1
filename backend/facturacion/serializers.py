from datetime import datetime

from .models import Cuota, Configuracion
from accounts.models import User
from accounts import utils


from rest_framework import serializers
from accounts.serializers import UserProfileSerializer


class CuotaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = ["id", "fecha", "created_by", "owner", "monto"]
        ordering = ["-fecha"]


class CuotaSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    created_by = UserProfileSerializer()
    fecha_format = serializers.SerializerMethodField()

    class Meta:
        model = Cuota
        fields = ["id", "fecha", "fecha_format", "created_by", "owner", "monto"]

    def get_fecha_format(self, obj):
        return obj.fecha.strftime("%d/%m/%Y - %H:%M")


class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = "__all__"
