from rest_framework import serializers

from accounts.models import User


class DetalleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'role', 'is_active']

    
