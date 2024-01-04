from datetime import timedelta, date
from django.utils import timezone
from rest_framework.decorators import action

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Reserva, Prestamo, ListaEspera
from accounts.models import User
from materiales.models import Material

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

        data = {
            "owner": owner.id,
            "material": material.id,            
        }
        serializer = ReservasSerializer(data=data)        
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
