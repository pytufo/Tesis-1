""" from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST """
# from rest_framework.exceptions import ValidationError

from .utils import (
    get_limite_reservas_prestamo,
    usuario_tiene_reserva_pendiente,
    get_reserva_proxima_a_espirar,
)
from materiales.utils import (
    get_estado,
)


from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo
from accounts.models import User
from materiales.models import Material
from materiales.serializers import EjemplarSerializer


# fake = Faker()

from .serializers import (
    ReservasSerializer,
    PrestamosSerializer,
)


# Create your views here.
""" @csrf_exempt
@require_POST
def create_fake(request):
    for _ in range(5):
        Reserva.objects.create(
            fecha_inicio=fake.date_between(start_date="-30d", end_date="today"),
            fecha_fin=fake.date_between(start_date="today", end_date="+30d"),
            owner=User.objects.order_by("?").first(),
            material=Material.objects.order_by("?").first(),
        )
    return JsonResponse({"message": "Datos aleatorios generados exitosamente"})

 """


class ReservaFilter(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservasSerializer
    # filterset_class = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ["material", "owner"]
    search_fields = ["material__titulo", "owner__email"]


class ReservaViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ReservasSerializer
    queryset = Reserva.objects.all()

    def create(self, request, *args, **kwargs):
        material_id = request.data.get("material")
        usuario_id = request.data.get("owner")

        material = Material.objects.get(pk=material_id)
        usuario = User.objects.get(pk=usuario_id)

        limite_reservas_prestamo = get_limite_reservas_prestamo(usuario)
        estado = get_estado(material)

        if usuario_tiene_reserva_pendiente(usuario, material):
            return Response({"message": "Ya tienes una reserva para este material..."})

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
            return Response(
                {"message": "No hay ejemeplares disponibles para la reserva. "}
            )

        if limite_reservas_prestamo == "Excede":
            return Response(
                {"message": "El usuario ha excedido el limite de reservas o prestamos"}
            )

        return super().create(request, *args, **kwargs)


class PrestamoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = PrestamosSerializer
    queryset = Prestamo.objects.all()


""" class ReservasSearchView(generics.ListAPIView):
    serializer_class = ListReservaSerializer

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        queryset = Reservas.objects.all()

        if query:
            # Realiza la búsqueda en el nombre del artículo, fecha y nombre de usuario
            queryset = queryset.filter(
                Q(material__nombre__icontains=query)
                | Q(fecha_fin__icontains=query)
                | Q(owner__username__icontains=query)
            )

        return queryset



class ReservaCreateView(generics.ListCreateAPIView):
    permission_classess = (IsAuthenticated,)
    serializer_class = CreateReservaserializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReservaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListReservaSerializer
    queryset = Reservas.objects.all()

    def retrieve(self, request, *args, **kwargs):
        super(ReservaDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully retrieved",
            "result": data,
        }
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(ReservaDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully updated",
            "result": data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(ReservaDetailView, self).delete(request, args, kwargs)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted",
        }
        return Response(response)


class CreatePrestamoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrestamosSerializer
    queryset = Prestamos.objects.all()


"""
