from rest_framework import (
    viewsets,
    status,
    generics,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsSuperUserOrReadOnly
from rest_framework.response import Response

from materiales.serializers import (
    ArticuloSerializer,
    TipoMaterialSerializer,
    AutorSerializer,
    CarreraSerializer,
    GeneroSerializer,
    EditorialSerializer,
    EjemplarSerializer,
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
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = CarreraSerializer
    queryset = Carrera.objects.all()


class GeneroViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = GeneroSerializer
    queryset = Genero.objects.all()


class EditorialViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = EditorialSerializer
    queryset = Editorial.objects.all()


class TipoMaterialViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = TipoMaterialSerializer
    queryset = TipoMaterial.objects.all()


class AutorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()


class ArticuloViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()


class EjemplarViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = EjemplarSerializer
    queryset = Ejemplar.objects.all()


""" 

class CreateArticuloView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()


class DetailArticuloView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        super(DetailArticuloView, self).retrieve(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Succesfully retrieved",
            "result": data,
        }
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(DetailArticuloView, self).patch(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Succesfully updated",
            "result": data,
        }
        return Response(response)


class CreateEjemplarView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = EjemplarSerializer
    queryset = Ejemplar.objects.all()


class DetailEjemplarView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EjemplarSerializer
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
 """
