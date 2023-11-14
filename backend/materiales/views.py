from rest_framework import (
    viewsets,
    status,
    generics,
    serializers,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from materiales.serializers import (
    ArticuloSerializer,
    ArticuloNameSerializer,
    ListArticuloSerializer,
    TipoMaterialSerializer,
    AutorSerializer,
    CarreraSerializer,
    GeneroSerializer,
    EditorialSerializer,
    ListEjemplarSerializer,
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
    serializer_class = ArticuloNameSerializer
    queryset = Articulo.objects.all()


class CreateArticuloView(generics.ListCreateAPIView):
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()


class DetailArticuloView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ListArticuloSerializer

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
    serializer_class = ListEjemplarSerializer
    queryset = Ejemplar.objects.all()


class CreateEjemplarView(generics.ListCreateAPIView):
    serializer_class = EjemplarSerializer
    queryset = Ejemplar.objects.all()


class DetailEjemplarView(generics.RetrieveUpdateDestroyAPIView):
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


class ListArticuloView(generics.ListAPIView):
    serializer_class = ListArticuloSerializer
    permission_classes = (AllowAny,)
    queryset = Articulo.objects.all()
