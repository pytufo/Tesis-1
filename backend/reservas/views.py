from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.db import transaction


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
    get_ejemplares_de_material,
    get_estado_ejemplar,
)


from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PrestamoFilter

# from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo, ListaEspera
from accounts.models import User
from materiales.models import Material, Ejemplar

# from materiales.serializers import EjemplarSerializer


# fake = Faker()

# from materiales.serializers import EjemplarSerializer

from .serializers import (
    ReservasSerializer,
    PrestamosSerializer,
    PrestamoCreateSerializer,
    ReservaCreateSerializer,
    ListaDeEsperaSerializer,
    EjemplarSerializer,
)


class ReservaViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ReservaCreateSerializer
    queryset = Reserva.objects.all()

    def retrieve_material(self, request, material_pk=None):
        material = Material.objects.get(pk=material_pk)
        serializer = MaterialSerializer(material)

        ejemplares = get_ejemplares_de_material(material)
        ejemplares_serializer = EjemplarSerializer(ejemplares, many=True)
        response_data = {
            "material": serializer.data,
            "ejemplares": ejemplares_serializer.data,
        }

        return Response(response_data)

    def create(self, request, material_pk=None):
        usuario_id = request.data.get("owner")

        material = Material.objects.get(pk=material_pk)
        usuario = User.objects.get(pk=usuario_id)

        limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)
        estado = get_estado(material)

        ### El usuario no podrá resepetir una reserva.

        if usuario_tiene_reserva_pendiente(usuario, material):
            return Response({"message": "Ya tienes una reserva para este material..."})

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

    #
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
    serializer_class = PrestamoCreateSerializer
    queryset = Prestamo.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = PrestamoFilter

    def retrieve_ejemplar(self, request, ejemplar_pk=None):
        ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)
        serializer = EjemplarSerializer(ejemplar)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def devolucion(self, request, pk=None):
        try:
            prestamo = self.get_object()

            """ if prestamo.fecha_fin is not None:
                return Response(
                    {"message": "El préstamo ya ha sido devuelto"},
                    status=status.HTTP_400_BAD_REQUEST,
                ) """

            prestamo.fecha_fin = timezone.now().date()
            prestamo.save()

            return Response(
                {"message": "Devolución exitosa"}, status=status.HTTP_200_OK
            )

        except Prestamo.DoesNotExist:
            return Response(
                {"message": "El préstamo no existe"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"Error al realizar la devolución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, ejemplar_pk=None):
        # definimos los campos de "prestamo"
        created_by_id = request.data.get("created_by")
        usuario_id = request.data.get("owner")
        ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)
        usuario = User.objects.get(pk=usuario_id)
        created_by = User.objects.get(pk=created_by_id)

        # definimos variables de estados y aplicamos sus validaciones
        estado = get_estado_ejemplar(ejemplar)
        limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)

        if estado == "En prestamo":
            return Response({"message": "El ejemplar ya se encuentra prestado"})
        if limite_reservas_prestamo == "Excede":
            return Response(
                {"message": "El usuario ha excedido el limite de reservas o prestamos"}
            )

        fecha_fin_default = (timezone.now() + timedelta(days=7)).date()

        # asignamos los valores a cargar en "prestamo"
        data = {
            "created_by": created_by.id,
            "owner": usuario.id,
            "ejemplar": ejemplar.id,
            "fecha_fin": fecha_fin_default,
        }

        serializer = PrestamoCreateSerializer(data=data, ejemplar_pk=ejemplar_pk)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data["fecha_fin"] = fecha_fin_default
        serializer.save(ejemplar=ejemplar)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Un prestamo puede ser de dos maneras: Presencial-inmediata o Retiro de reserva
