from datetime import timedelta, date
from django.utils import timezone
from rest_framework.decorators import action

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Reserva, Prestamo, ListaEspera
from accounts.models import User
from materiales.models import Material, Ejemplar

from .serializers import (
    ReservasSerializer,
    PrestamosSerializer,
    ListaDeEsperaSerializer,
)


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservasSerializer
    queryset = Reserva.objects.all()


class ReservaFilter(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservasSerializer
    # filterset_class = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ["material", "owner"]
    search_fields = ["material__titulo", "owner__email"]


class PrestamoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = PrestamosSerializer
    queryset = Prestamo.objects.all()

    def retrieve(self, request, reserva_pk=None):
        reserva = Reserva.objects.get(pk=reserva_pk)
        owner = reserva.owner
        material = reserva.material
        fecha_fin = reserva.fecha_fin
        reserva_data = {
            "fecha_fin": fecha_fin,
            "owner": owner.id,
            "material": material.id,
        }

        reserva_serializer = ReservasSerializer(data=reserva_data)
        reserva_serializer.is_valid(raise_exception=True)
        return Response(reserva_serializer.data)

    @action(detail=True, methods=["post"])
    def create_prestamo(self, request, reserva_pk=None):
        # Obtener la reserva y ejemplares asociados
        reserva = Reserva.objects.get(pk=reserva_pk)
        material = reserva.material
        ejemplares = Ejemplar.objects.filter(material=material)

        # Obtener el ejemplar seleccionado del request
        ejemplar_id = request.data.get(
            "ejemplar_id"
        )  # Asegúrate de tener el nombre correcto
        ejemplar = Ejemplar.objects.get(pk=ejemplar_id)


""" 
    @action(detail=True, methods=["post"])
    def create(self, request, reserva_pk=None):
        usuario_admin = request.data.get("created_by")
        usuario = request.data.get("owner")

        ejemplar = Ejemplar.objects.get """
