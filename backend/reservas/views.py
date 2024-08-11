from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator


from django.views.decorators.csrf import csrf_protect
from datetime import timedelta, date, datetime
from django.utils import timezone
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from materiales.serializers import MaterialSerializer
from .utils import (
    get_limite_reservas_prestamo,
    usuario_tiene_reserva_prestamo_pendiente,
    habilitar_reserva_lista_espera,
    get_estado_prestamo,
    get_estado_reserva,
)
from materiales.utils import (
    get_estado,
    get_ejemplares_disponibles,
    get_estado_ejemplar,
)

from rest_framework import viewsets, filters, generics, status

# from rest_framework.response import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PrestamoFilter

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated

# from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo
from accounts.models import User
from materiales.models import Material, Ejemplar


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
        usuario = request.user
        query = request.GET.get("query", "")

        if usuario.role == 1 or usuario.role == 2:
            reservas = Reserva.objects.all()
        else:
            reservas = Reserva.objects.filter(owner=usuario.id)

        if query:
            reservas = reservas.filter(
                Q(material__titulo__icontains=query)
                | Q(owner__id__icontains=query)
                | Q(owner__email__icontains=query)
                | Q(owner__first_name__icontains=query)
                | Q(owner__last_name__icontains=query)
            )
        # reservas = Reserva.objects.filter(fecha_fin__isnull=False)
        paginator = Paginator(reservas, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        reservas_serializer = ReservasSerializer(page_obj, many=True)
        serializer_reservas = reservas_serializer.data

        return render(
            request,
            "reservas/listar_reservas.html",
            {"page_obj": page_obj, "reservas": serializer_reservas, "query": query},
        )

        return JsonResponse(serializer.data)

    @action(detail=False, methods=["GET"])
    def listar_reservas_usuario(self, request, *args, **kwargs):
        usuario = request.user
        query = request.GET.get("query", "")

        reservas = Reserva.objects.filter(owner=usuario.id)

        if query:
            reservas = reservas.filter(
                Q(material__titulo__icontains=query)
                | Q(owner__email__icontains=query)
                | Q(owner__first_name__icontains=query)
                | Q(owner__last_name__icontains=query)
            )
        # reservas = Reserva.objects.filter(fecha_fin__isnull=False)
        paginator = Paginator(reservas, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        reservas_serializer = ReservasSerializer(page_obj, many=True)
        serializer_reservas = reservas_serializer.data

        return render(
            request,
            "reservas/listar_reservas.html",
            {"page_obj": page_obj, "reservas": serializer_reservas, "query": query},
        )

    # @action(detail=True, methods=["put"])
    # @csrf_protect
    def cancelar_reserva(self, request, pk=None):
        if request.method == "POST":
            try:
                reserva = self.get_object()

                estado = get_estado_reserva(reserva)
                if estado == "Finalizada":
                    return JsonResponse(
                        {"message": "La reserva ya ha expirado"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                fecha_fin_anterior = reserva.fecha_fin
                reserva.fecha_fin = timezone.now()
                reserva.save()

                habilitar_reserva_lista_espera(reserva.material, fecha_fin_anterior)
                return JsonResponse(
                    {"message": "Reserva cancelada. ", "status": 200, "success": True}
                )

            except Reserva.DoesNotExist:
                return JsonResponse(
                    {"message": "la reserva no existe", "success": False},
                    status=status.HTTP_404_NOT_FOUND,
                )

            except Exception as e:
                return JsonResponse(
                    {"message": f"Error al realizar la cancelación: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return redirect("/")

    def retrieve(self, request, pk=None):
        reserva = Reserva.objects.get(pk=pk)
        serializer = ReservasSerializer(reserva)
        return JsonResponse(serializer.data)

    def detalle_reserva(self, request, reserva_pk=None):
        reserva_id = Reserva.objects.get(pk=reserva_pk)
        reserva = ReservasSerializer(reserva_id)
        return render(
            request,
            "reservas/detalle_reserva.html",
            {
                "reserva": reserva.data,
            },
        )

    def retrieve_material(self, request, *args, **kwargs):
        try:
            reserva = self.get_object()
            material = reserva.material

            ejemplares_disponibles = get_ejemplares_disponibles(material)

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

            return JsonResponse(response_data)

        except Reserva.DoesNotExist:
            return JsonResponse(
                {"message": "La reserva no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return JsonResponse(
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

            reserva_prestamo_pendiente = usuario_tiene_reserva_prestamo_pendiente(
                usuario, material
            )
            if reserva_prestamo_pendiente:
                if reserva_prestamo_pendiente["tipo"] == "Prestamo":
                    message = "Ya tienes un prestamo con este material."
                elif reserva_prestamo_pendiente["tipo"] == "Reserva":
                    message = "Ya tienes una reserva con este material."
                return JsonResponse(
                    {
                        "message": message,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ### Obtenemos el estado del material dando opcion para una "lista de espera" obteniendo el material proximo a liberarse.
            ### solicitando una confirmacion para crearla

            if estado == "Disponible (Lista de espera)":
                fecha_fin_default = None
            elif estado == "No disponible (Solo lectura)":
                return JsonResponse(
                    {
                        "message": "El material no cuenta con ejemplares disponibles para la reserva."
                    }
                )

            else:
                fecha_fin_default = timezone.now() + timedelta(days=1)

            if limite_reservas_prestamo == "Excede":
                return JsonResponse(
                    {
                        "message": "El usuario ha excedido el limite de reservas o prestamos"
                    }
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

            return JsonResponse(
                {
                    "message": "Reserva creada con exito",
                    "id": serializer.data["id"],
                    "success": True,
                },
            )
        except Material.DoesNotExist:
            return JsonResponse({"message": "El material no existe", "success": False})

        except Exception as e:
            return JsonResponse(
                {"message": f"Error al obtener información de la reserva: {str(e)}"}
            )


class PrestamoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = PrestamoCreateSerializer
    queryset = Prestamo.objects.all()

    def list(self, request, *args, **kwargs):
        usuario = request.user
        query = request.GET.get("query", "")

        if usuario.role == 1 or usuario.role == 2:
            prestamos = Prestamo.objects.all()
        else:
            prestamos = Prestamo.objects.filter(owner=usuario.id)

        if query:
            prestamos = prestamos.filter(
                Q(ejemplar__material__titulo__icontains=query)
                | Q(owner__id__icontains=query)
                | Q(owner__email__icontains=query)
                | Q(owner__first_name__icontains=query)
                | Q(owner__last_name__icontains=query)
            )
        # reservas = Reserva.objects.filter(fecha_fin__isnull=False)
        paginator = Paginator(prestamos, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        prestamos_serializer = PrestamosSerializer(page_obj, many=True)
        serializer_prestamos = prestamos_serializer.data

        return render(
            request,
            "prestamos/listar_prestamos.html",
            {"page_obj": page_obj, "prestamos": serializer_prestamos, "query": query},
        )

    @action(detail=False, methods=["GET"])
    def listar_prestamos_usuario(self, request, *args, **kwargs):
        usuario = request.user
        query = request.GET.get("query", "")

        prestamos = Prestamo.objects.filter(owner=usuario.id)

        if query:
            prestamos = prestamos.filter(
                Q(ejemplar__material__titulo__icontains=query)
                | Q(owner__id__icontains=query)
                | Q(owner__email__icontains=query)
                | Q(owner__first_name__icontains=query)
                | Q(owner__last_name__icontains=query)
            )
        # reservas = Reserva.objects.filter(fecha_fin__isnull=False)
        paginator = Paginator(prestamos, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        prestamos_serializer = PrestamosSerializer(page_obj, many=True)
        serializer_prestamos = prestamos_serializer.data

        return render(
            request,
            "prestamos/listar_prestamos.html",
            {"page_obj": page_obj, "prestamos": serializer_prestamos, "query": query},
        )

    def detalle_prestamo(self, request, prestamo_pk=None):
        prestamo_id = Prestamo.objects.get(pk=prestamo_pk)
        prestamo = PrestamosSerializer(prestamo_id)
        return render(
            request,
            "prestamos/detalle_prestamo.html",
            {
                "prestamo": prestamo.data,
            },
        )

    def retrieve(self, request, pk=None):
        prestamo = Prestamo.objects.get(pk=pk)
        serializer = PrestamosSerializer(prestamo)
        return JsonResponse(serializer.data)

    @action(detail=True, methods=["get"])
    def retrieve_ejemplar(self, request, ejemplar_pk=None):
        ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)
        serializer = EjemplarSerializer(ejemplar)
        return JsonResponse(serializer.data)

    # @action(detail=True, methods=["put"])
    def devolucion(self, request, pk=None):
        try:
            prestamo = self.get_object()

            estado = get_estado_prestamo(prestamo)

            if estado == "Finalizado":
                return JsonResponse(
                    {"message": "El prestamo ya ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            fecha_fin_anterior = prestamo.fecha_fin
            prestamo.fecha_fin = timezone.now()
            prestamo.save()
            habilitar_reserva_lista_espera(
                prestamo.ejemplar.material, fecha_fin_anterior
            )
            return JsonResponse(
                {"success": True, "message": "Devolución exitosa"},
                status=status.HTTP_200_OK,
            )

        except Prestamo.DoesNotExist:
            return JsonResponse(
                {"message": "El préstamo no existe"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return JsonResponse(
                {"message": f"Error al realizar la devolución: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Un prestamo puede ser de dos maneras: Presencial-inmediata o Entrega de reserva
    # @action(detail=False, methods=["post"])
    def create(self, request):
        try:
            # definimos los campos de "prestamo"
            usuario_id = request.data.get("owner")
            usuario = User.objects.get(email=usuario_id)
            ejemplar_id = request.data.get("ejemplar") or request.data.get("IdEjemplar")
            ejemplar = Ejemplar.objects.get(pk=ejemplar_id)

            if get_estado(ejemplar.material) != "Disponible":
                return JsonResponse(
                    {"message": "El material no cuenta con ejemplares disponibles para realizar prestamo"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # definimos variables de estados y aplicamos sus validaciones
            estado = get_estado_ejemplar(ejemplar)
            limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)

            # Verificar si el usuario tiene una reserva o prestamo pendiente par el mismo material
            pendiente = usuario_tiene_reserva_prestamo_pendiente(
                usuario, ejemplar.material
            )
            if pendiente:   
                tipo = pendiente["tipo"]
                if tipo == "Reserva":
                    return JsonResponse(
                        {
                            "message": "El usuario ya tiene una reserva vigente para este material"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif tipo == "Prestamo":
                    return JsonResponse(
                        {
                            "message": "El usuario ya tiene prestamo vigente para este material"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            if estado == "En prestamo":
                return JsonResponse({"message": "El ejemplar ya se encuentra prestado"})
            if limite_reservas_prestamo == "Excede":
                return JsonResponse(
                    {
                        "message": "El usuario ha excedido el limite de reservas o prestamos"
                    }
                )

            fecha_fin_default = timezone.now() + timedelta(days=7)
            if not usuario.is_active:
                return JsonResponse({
                    "message": "El usuario a efectuar el prestamo no se encuentra habilidado para esta accion"
                })
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

            return JsonResponse(
                {"message": "Prestamo creado con exito", "success": True},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return JsonResponse(
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

            return JsonResponse(response_data)

        except Reserva.DoesNotExist:
            return JsonResponse(
                {"message": "La reserva no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return JsonResponse(
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
                return JsonResponse(
                    {"message": "La reserva ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not ejemplares_disponibles:
                return JsonResponse(
                    {"message": "No se encuentran ejemplares disponibles"}
                )
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

            return JsonResponse(
                {"success": True, "message": "El prestamo ha sido creado"},
                status=status.HTTP_201_CREATED,
            )

        except Reserva.DoesNotExist:
            return JsonResponse(
                {"message": "La reserva no existe"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return JsonResponse(
                {"message": f"Error al entregar ejemplar desde reserva: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
