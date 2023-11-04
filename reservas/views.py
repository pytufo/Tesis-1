from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count, Sum, Q

from .models import Reservas, Prestamos

from .serializers import (ListReservaSerializer, PrestamosSerializer, ReservasSerializer, CreateReservaserializer)
# Create your views here.


class ReservasView(generics.ListAPIView):
    serializer_class = ListReservaSerializer
    queryset = Reservas.objects.all()


class ReservasSearchView(generics.ListAPIView):
    serializer_class = ListReservaSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        queryset = Reservas.objects.all()

        if query:
            # Realiza la búsqueda en el nombre del artículo, fecha y nombre de usuario
            queryset = queryset.filter(
                Q(articulo__nombre__icontains=query) |
                Q(fecha_fin__icontains=query) |
                Q(owner__username__icontains=query)
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
