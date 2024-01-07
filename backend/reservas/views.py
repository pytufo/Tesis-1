from django.http import QueryDict
from datetime import timedelta, date
from django.utils import timezone
from rest_framework.decorators import action

from materiales.serializers import MaterialSerializer
from .utils import (
    get_limite_reservas_prestamo,
    usuario_tiene_reserva_pendiente,
    get_reserva_proxima_a_espirar,
    get_limite_epera,
)
from materiales.utils import (
    get_estado,
)


from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo, ListaEspera
from accounts.models import User
from materiales.models import Material

# from materiales.serializers import EjemplarSerializer


# fake = Faker()

from .serializers import (
    ReservasSerializer,
    PrestamosSerializer,
    ReservaCreateSerializer,
    ListaDeEsperaSerializer,
)


class ReservaFilter(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservasSerializer
    # filterset_class = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ["material", "owner"]
    search_fields = ["material__titulo", "owner__email"]


class ReservaViewSet(viewsets.ViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ReservaCreateSerializer
    # queryset = Reserva.objects.all()

    def retrieve(self, request, material_pk=None):
        material = Material.objects.get(pk=material_pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def create(self, request, material_pk=None):
        usuario_id = request.data.get("owner")

        material = Material.objects.get(pk=material_pk)
        usuario = User.objects.get(pk=usuario_id)

        limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)
        estado = get_estado(material)

        ### El usuario no podrá resepetir una reserva.

        if usuario_tiene_reserva_pendiente(usuario, material):
            return Response(
                {"message": "Ya tienes una reserva para este material..."}
            )

        ### Obtenemos el estado del material dando opcion para una "lista de espera" obteniendo el material proximo a liberarse.
        ### solicitando una confirmacion para crearla

        if estado == "No Disponible" or estado == "Lectura":
            reserva_proxima = get_reserva_proxima_a_espirar(material)
            if reserva_proxima:
                serializer = ReservasSerializer(reserva_proxima)
                return Response(
                    {
                        "message": "No hay ejemplares disponibles para la reserva. Reserva próxima a expirar:",
                        "reserva_proxima": serializer.data,
                    }
                )
            else:
                return Response(
                    {"message": "No hay ejemplares disponibles para la reserva. "}
                )

        if limite_reservas_prestamo == "Excede":
            return Response(
                {"message": "El usuario ha excedido el limite de reservas o prestamos"}
            )

        ### Establecemos un limite para la "fecha_fin" por defecto de 1 dia.
        fecha_fin_default = (timezone.now() + timedelta(days=1)).date()

        data = {
            "owner": usuario.id,
            "material": material.id,
            "fecha_fin": fecha_fin_default,
        }

        # data = request.data.copy()
        # data["fecha_fin"] = fecha_fin_default

        serializer = ReservaCreateSerializer(data=data, material_pk=material_pk)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data["fecha_fin"] = fecha_fin_default
        serializer.save(material=material)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListaDeEsperaviewset(viewsets.ModelViewSet):
    serializer_class = ListaDeEsperaSerializer
    queryset = ListaEspera.objects.all()

    def retrieve(self, request, material_pk=None):
        material = Material.objects.get(pk=material_pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def create(self, request, material_pk=None):
        usuario_id = request.data.get("owner")
        material = Material.objects.get(pk=material_pk)
        usuario = User.objects.get(pk=usuario_id)

        ### Establecemos un limite para la "fecha_fin" por defecto de 1 dia.
        fecha_fin_default = (timezone.now() + timedelta(days=1)).date()
        limite_espera = get_limite_epera(material)

        if limite_espera == 0:
            return Response(
                {
                    "message": "La cola de espera se encuetra llena, por favor intente denuevo más tarde."
                }
            )
        data = {
            "owner": usuario.id,
            "material": material.id,
            "fecha_fin": fecha_fin_default,
        }

        serializer = ListaDeEsperaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data["fecha_fin"] = fecha_fin_default
        serializer.save(material=material)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrestamoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = PrestamosSerializer
    queryset = Prestamo.objects.all()
