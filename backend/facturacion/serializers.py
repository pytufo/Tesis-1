from .models import Cuota
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
    class Meta:
        model = Cuota
        fields = ["id", "fecha", "created_by", "owner", "monto"]
