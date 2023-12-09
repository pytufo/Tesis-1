from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .utils import get_cantidad_existente, get_cantidad_disponible
from materiales.models import Material, Editorial, Autor, TipoMaterial, Genero, Carrera
from rest_framework import (
    viewsets,
    generics,
)

fake = Faker()

from rest_framework.permissions import AllowAny
from .permissions import IsSuperUserOrReadOnly


from materiales.serializers import (
    MaterialSerializer,
    TipoMaterialSerializer,
    AutorSerializer,
    CarreraSerializer,
    GeneroSerializer,
    EditorialSerializer,
    EjemplarSerializer,
)

from accounts.models import User
from materiales.models import (
    Material,
    Ejemplar,
    TipoMaterial,
    Autor,
    Carrera,
    Genero,
    Editorial,
)


@csrf_exempt
@require_POST
def generar_datos_aleatorios(request):
    for _ in range(5):
        Editorial.objects.create(nombre=fake.company())

    for _ in range(10):
        Autor.objects.create(nombre=fake.first_name(), apellido=fake.last_name())

    for _ in range(3):
        TipoMaterial.objects.create(nombre=fake.word())

    for _ in range(3):
        Genero.objects.create(nombre=fake.word())

    for _ in range(5):
        Carrera.objects.create(nombre=fake.word())

    for _ in range(10):
        material = Material.objects.create(
            titulo=fake.sentence(),
            descripcion=fake.paragraph(),
        )
        material.editorial.set(Editorial.objects.order_by("?")[:3])
        material.autor.set(Autor.objects.order_by("?")[:2])
        material.tipo.set(TipoMaterial.objects.order_by("?")[:1])
        material.genero.set(Genero.objects.order_by("?")[:1])
        material.carrera.set(Carrera.objects.order_by("?")[:1])
    for _ in range(20):
        material = Material.objects.order_by("?")[:1].first()
        Ejemplar.objects.create(
            material=material,
            estado=fake.boolean(),
        )
    return JsonResponse({"message": "Datos aleatorios generados exitosamente"})


class CarreraViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = CarreraSerializer
    queryset = Carrera.objects.all()


class GeneroViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = GeneroSerializer
    queryset = Genero.objects.all()


class EditorialViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = EditorialSerializer
    queryset = Editorial.objects.all()


class TipoMaterialViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = TipoMaterialSerializer
    queryset = TipoMaterial.objects.all()


class AutorViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()


class MaterialViewSet(viewsets.ModelViewSet):
    # permission_classes = (AllowAny, IsSuperUserOrReadOnly)
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()


class EjemplarViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = EjemplarSerializer
    queryset = Ejemplar.objects.all()


class DetalleEjemplar(generics.ListAPIView):
    queryset = Ejemplar.objects.all()
    serializer_class = EjemplarSerializer


""" 

class CreateMaterialView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()


class DetailMaterialView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()

    def retrieve(self, request, *args, **kwargs):
        super(DetailMaterialView, self).retrieve(request, *args, **kwargs)
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
        super(DetailMaterialView, self).patch(request, *args, **kwargs)
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
