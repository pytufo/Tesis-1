""" from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST """
# from rest_framework.exceptions import ValidationError

from materiales.utils import get_estado

from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Reserva, Prestamo
from accounts.models import User
from materiales.models import Articulo
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
            articulo=Articulo.objects.order_by("?").first(),
        )
    return JsonResponse({"message": "Datos aleatorios generados exitosamente"})

 """


class ArticuloFilter(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservasSerializer
    # filterset_class = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ["articulo", "owner"]
    search_fields = ["articulo__titulo", "owner__email"]


class ReservaViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ReservasSerializer
    queryset = Reserva.objects.all()

    def create(self, request, *args, **kwargs):
        articulo_id = request.data.get("articulo")
        articulo = Articulo.objects.get(pk=articulo_id)

        estado = get_estado(articulo)
        if estado:
            "No disponible"
            return Response(
                {"message": "No hay ejemeplares disponibles para la reserva. "}
            )
        return super().create(request, *args, **kwargs)
        """ cantidad_disponible = get_cantidad_disponible(articulo)
        if cantidad_disponible < 1:
            return Response(
                {
                    "message": "No hay ejemeplares disponibles para la reserva. ¿Desea colocarse en la proxima lista de espera?"
                }
            )
        return super().create(request, *args, **kwargs)
 """


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
                Q(articulo__nombre__icontains=query)
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
