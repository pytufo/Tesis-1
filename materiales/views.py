from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, authentication, permissions, generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Sum, Q



from . import serializers
from rest_framework.permissions import IsAuthenticated
from materiales.serializers import (
    ArticuloSerializer,
    
    TipoMaterialSerializer,
    AutorSerializer,
    CarreraSerializer,
    GeneroSerializer,
    EditorialSerializer,

)

from accounts.models import User
from materiales.models import (
    Articulo,
    Ejemplar,
    TipoMaterial,
    Autor,
    Carrera,
    Genero,
    Editorial,
)

class CarreraViewSet(viewsets.ModelViewSet):
    serializer_class = CarreraSerializer
    queryset = Carrera.objects.all()


class GeneroViewSet(viewsets.ModelViewSet):
    serializer_class = GeneroSerializer
    queryset = Genero.objects.all()


class EditorialViewSet(viewsets.ModelViewSet):
    serializer_class = EditorialSerializer
    queryset = Editorial.objects.all()


class TipoMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = TipoMaterialSerializer
    queryset = TipoMaterial.objects.all()


class AutorViewSet(viewsets.ModelViewSet):
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()


class TituloView(generics.ListAPIView):
    serializer_class = serializers.ArticuloNameSerializer
    queryset = Articulo.objects.all()


class CreateArticuloView(generics.ListCreateAPIView):

    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()


class DetailArticuloView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = serializers.ListArticuloSerializer

    def retrieve(self, request, *args, **kwargs):
        super(DetailArticuloView, self).retrieve(request, args, kwargs)
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
        super(DetailArticuloView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully updated",
            "result": data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(DetailArticuloView, self).delete(request, args, kwargs)
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted",
        }
        return Response(response)


class ListEjemplarView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ListEjemplarSerializer
    queryset = Ejemplar.objects.all()


class CreateEjemplarView(generics.ListCreateAPIView):
    serializer_class = serializers.EjemplarSerializer
    queryset = Ejemplar.objects.all()


class DetailEjemplarView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.EjemplarSerializer
    queryset = Ejemplar.objects.all()

    def retrieve(self, request, *args, **kwargs):
        super(DetailEjemplarView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully retrieved",
            "Ejemplar": data,
        }
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(DetailEjemplarView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully updated",
            "Ejemplar": data,
        }
        return Response(response)


"""    user = request.user
    articulo = self.get_object()
    serializer = ArticuloSerializer(data=request.data)
    if user.role == 5:
"""


class ListArticuloView(generics.ListAPIView):
    serializer_class = serializers.ListArticuloSerializer
    permission_classes = (AllowAny,)
    queryset = Articulo.objects.all()

"""     stock = Ejemplar.objects.values('articulo').annotate(
        cant_ejemplares=Count('articulo'),
        cant_disponibles=Count('estado', filter=Q(estado='d'))
    )
    for item in stock:      
            if item['cant_disponibles'] > 0:       
                print(item)
                print(item['articulo'], item['cant_disponibles'])
 """
