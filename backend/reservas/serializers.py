from rest_framework import serializers


from .models import Reserva, Prestamo


class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = "__all__"


