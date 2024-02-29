from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.db import transaction


from datetime import timedelta, date, datetime
from django.utils import timezone
from rest_framework.decorators import action

from materiales.serializers import MaterialSerializer
from .utils import (
    get_limite_reservas_prestamo,
    usuario_tiene_reserva_pendiente,
    habilitar_reserva_lista_espera,
    get_estado_prestamo,
    get_estado_reserva,
)
from materiales.utils import (
    get_estado,
    get_ejemplares_de_material,
    get_ejemplares_disponibles,
    get_estado_ejemplar,
)


from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PrestamoFilter

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo
from accounts.models import User
from materiales.models import Material, Ejemplar

# from materiales.serializers import EjemplarSerializer


# fake = Faker()

# from materiales.serializers im port EjemplarSerializer

from .serializers import (
    ReservasSerializer,
    PrestamosSerializer,
    EntregaEjemplarReserva,
    PrestamoCreateSerializer,
    ReservaCreateSerializer,
    EjemplarSerializer,
)


class ReservaViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReservaCreateSerializer
    queryset = Reserva.objects.all()

    def list(self, request, *args, **kwargs):
        reservas = Reserva.objects.filter(fecha_fin__isnull=False)
        serializer = ReservasSerializer(
            reservas, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def listar_reservas_usuario(self, request, *args, **kwargs):
        usuario = request.user

        try:
            reservas_usuario = Reserva.objects.filter(owner=usuario)
            serializer = ReservasSerializer(
                reservas_usuario, context={"request": request}, many=True
            )
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"message": f"Error al obtener las reservas del usuario: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["put"])
    def cancelar_reserva(self, request, pk=None):
        try:
            reserva = self.get_object()

            estado = get_estado_reserva(reserva)
            if estado == "Finalizada":
                return Response(
                    {"message": "La reserva ya ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            fecha_fin_anterior = reserva.fecha_fin
            reserva.fecha_fin = timezone.now()
            reserva.save()

            habilitar_reserva_lista_espera(reserva.material, fecha_fin_anterior)
            return Response(
                {"message": "Reserva cancelada. "}, status=status.HTTP_200_OK
            )

        except Reserva.DoesNotExist:
            return Response(
                {"message": "la reserva no existe"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"Error al realizar la cancelación: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        reserva = Reserva.objects.get(pk=pk)
        serializer = ReservasSerializer(reserva)
        return Response(serializer.data)

    def retrieve_material(self, request, *args, **kwargs):
        try:
            reserva = self.get_object()
            material = reserva.material

            ejemplares_disponibles = get_ejemplares_disponibles(material)

            # Puedes adaptar la lógica según tus necesidades para obtener ejemplares disponibles

            # Aquí devuelves la información sobre el material y ejemplares disponibles
            serializer_material = MaterialSerializer(
                material, context={"request": request}
            )
            serializer_ejemplares = EjemplarSerializer(
                ejemplares_disponibles, many=True, context={"request": request}
            )

            response_data = {
                "material": serializer_material.data,
                "ejemplares_disponibles": serializer_ejemplares.data,
            }

            return Response(response_data)

        except Reserva.DoesNotExist:
            return Response(
                {"message": "La reserva no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"Error al obtener información de la reserva: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, material_pk=None):
        usuario = request.user
        try:

            material = Material.objects.get(pk=material_pk)

            limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)
            estado = get_estado(material)

            ### El usuario no podrá resepetir una reserva.

            if usuario_tiene_reserva_pendiente(usuario, material):
                return Response(
                    {"message": "Ya tienes una reserva para este material..."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ### Obtenemos el estado del material dando opcion para una "lista de espera" obteniendo el material proximo a liberarse.
            ### solicitando una confirmacion para crearla

            if (
                estado == "Disponible (Lista de espera)"
                or estado == "Solo Lectura (Lista de espera)"
            ):
                fecha_fin_default = None
            else:
                fecha_fin_default = timezone.now() + timedelta(days=1)

            if limite_reservas_prestamo == "Excede":
                return Response(
                    {
                        "message": "El usuario ha excedido el limite de reservas o prestamos"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

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

            return Response(
                {"message": "Reserva creada con exito"}, status=status.HTTP_201_CREATED
            )
        except Material.DoesNotExist:
            return Response(
                {"message": "La reserva no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"Error al obtener información de la reserva: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PrestamoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = PrestamoCreateSerializer
    queryset = Prestamo.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = PrestamoFilter

    def list(self, request, *args, **kwargs):
        prestamos = Prestamo.objects.all()
        serializer = PrestamosSerializer(
            prestamos, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def listar_prestamos_usuario(self, request, *args, **kwargs):
        usuario = request.user

        try:
            reservas_usuario = Prestamo.objects.filter(owner=usuario)
            serializer = PrestamosSerializer(
                reservas_usuario, context={"request": request}, many=True
            )
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"message": f"Error al obtener los prestamos del usuario: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        prestamo = Prestamo.objects.get(pk=pk)
        serializer = PrestamosSerializer(prestamo)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def retrieve_ejemplar(self, request, ejemplar_pk=None):
        ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)
        serializer = EjemplarSerializer(ejemplar)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def devolucion(self, request, pk=None):
        try:
            prestamo = self.get_object()

            estado = get_estado_prestamo(prestamo)
            if estado == "Finalizado":
                return Response(
                    {"message": "El prestamo ya ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            fecha_fin_anterior = prestamo.fecha_fin
            prestamo.fecha_fin = timezone.now()
            prestamo.save()
            habilitar_reserva_lista_espera(
                prestamo.ejemplar.material, fecha_fin_anterior
            )
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

    # Un prestamo puede ser de dos maneras: Presencial-inmediata o Entrega de reserva
    # @action(detail=False, methods=["post"])
    def create(self, request, ejemplar_pk=None):
        try:
            # definimos los campos de "prestamo"
            usuario_id = request.data.get("owner")
            usuario = User.objects.get(pk=usuario_id)
            ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)

            # definimos variables de estados y aplicamos sus validaciones
            estado = get_estado_ejemplar(ejemplar)
            limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)

            if estado == "En prestamo":
                return Response({"message": "El ejemplar ya se encuentra prestado"})
            if limite_reservas_prestamo == "Excede":
                return Response(
                    {
                        "message": "El usuario ha excedido el limite de reservas o prestamos"
                    }
                )

            fecha_fin_default = timezone.now() + timedelta(days=7)

            # asignamos los valores a cargar en "prestamo"
            data = {
                "created_by": request.user.id,
                "owner": usuario.id,
                "ejemplar": ejemplar.id,
                "fecha_fin": fecha_fin_default,
            }

            serializer = PrestamoCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data["fecha_fin"] = fecha_fin_default
            serializer.save(ejemplar=ejemplar)

            return Response(
                {"message": "Prestamo creado con exito"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"message": f"Error al obtener informacion del prestamo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve_reserva(self, request, reserva_pk=None):
        try:
            reserva = Reserva.objects.get(pk=reserva_pk)
            material = reserva.material
            ejemplares_disponibles = Ejemplar.objects.filter(material=material)

            serializer_reserva = ReservasSerializer(reserva)
            serializer_ejemplares = EjemplarSerializer(
                ejemplares_disponibles, many=True, context={"request": request}
            )

            response_data = {
                "reserva": serializer_reserva.data,
                "ejemplares_disponibles": serializer_ejemplares.data,
            }

            return Response(response_data)

        except Reserva.DoesNotExist:
            return Response(
                {"message": "La reserva no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"Error al procesar la solicitud: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def entregar_ejemplar_reserva(self, request, reserva_pk=None):
        try:
            reserva = get_object_or_404(Reserva, pk=reserva_pk)
            ejemplares_disponibles = Ejemplar.objects.filter(material=reserva.material)

            created_by = request.user
            owner = reserva.owner
            fecha_fin_reserva = reserva.fecha_fin

            if fecha_fin_reserva < timezone.now():
                return Response(
                    {"message": "La reserva ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not ejemplares_disponibles:
                return Response({"message": "No se encuentran ejemplares disponibles"})
            fecha_fin_default = timezone.now() + timedelta(days=7)

            #
            prestamo_data = {
                "created_by": created_by.id,
                "ejemplar": ejemplares_disponibles.first().id,
                "owner": owner.id,
                "fecha_fin": fecha_fin_default,
            }

            serializer = PrestamoCreateSerializer(data=prestamo_data)
            serializer.is_valid(raise_exception=True)

            # Guardar el préstamo
            serializer.save()

            reserva = Reserva.objects.get(id=reserva_pk)
            reserva.fecha_fin = timezone.now()
            reserva.save()

            return Response(
                {"message": "El prestamo ha sido creado"},
                status=status.HTTP_201_CREATED,
            )

        except Reserva.DoesNotExist:
            return Response(
                {"message": "La reserva no existe"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": f"Error al entregar ejemplar desde reserva: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
