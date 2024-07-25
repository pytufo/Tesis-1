from faker import Faker
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

from .utils import (
    get_cantidad_existente,
    get_cantidad_disponible,
    get_ejemplares_de_material,
)
from materiales.models import Material, Editorial, Autor, TipoMaterial, Genero, Carrera
from rest_framework import (
    viewsets,
    generics,
)


from rest_framework.response import Response


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
    EjemplarMaterialSerializer,
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


def generar_pdf_material(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    response = HttpResponse(content_type="application/pdf")
    response["content-Disposition"] = (
        f'attachment; filename="material_{material_pk}.pdf"'
    )

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"ID del Material: {material.id}")

    p.drawString(100, height - 120, f"Titulo: {material.titulo}")

    p.drawString(100, height - 140, "Autor:")
    y = height - 160
    for autor in material.autor.all():
        p.drawString(120, y, f"{autor.nombre} {autor.apellido}")
        y -= 20

    p.drawString(100, y, "Tipo:")
    y -= 20
    for tipo in material.tipo.all():
        p.drawString(120, y, tipo.nombre)
        y -= 20

    p.drawString(100, y, "Genero:")
    y -= 20
    for genero in material.genero.all():
        p.drawString(120, y, genero.nombre)
        y -= 20

    p.drawString(100, y, "Editorial:")
    y -= 20
    for editorial in material.editorial.all():
        p.drawString(120, y, editorial.nombre)
        y -= 20

    p.drawString(100, y, "Carrera:")
    y -= 20
    for carrera in material.carrera.all():
        p.drawString(120, y, carrera.nombre)
        y -= 20

    p.drawString(100, y, f"Descripción: ")
    y -= 20
    descripcion_lines = simpleSplit(material.descripcion, "Helvetica", 12, width - 150)
    for line in descripcion_lines:
        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 100
        p.drawString(120, y, line)
        y -= 20

    p.showPage()
    p.save()

    return response


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
    permission_classes = (AllowAny,)
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()

    def listar_materiales(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        tipo = TipoMaterial.objects.all()
        editorial = Editorial.objects.all()
        autor = Autor.objects.all()
        carrera = Carrera.objects.all()
        genero = Genero.objects.all()
        ordering = request.GET.get("ordering", "titulo")
        if query:
            materiales = Material.objects.filter(
                Q(titulo__icontains=query)
                | Q(autor__nombre__icontains=query)
                | Q(descripcion__icontains=query)
            ).distinct()
        else:
            materiales = Material.objects.all()

        paginator = Paginator(materiales, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        materials_serializer = MaterialSerializer(page_obj, many=True)
        serializer_materials = materials_serializer.data
        return render(
            request,
            "materiales/listar_materiales.html",
            {
                "page_obj": page_obj,
                "query": query,
                "materials": serializer_materials,
                "materiales": materiales,
                "tipos": tipo,
                "editoriales": editorial,
                "autores": autor,
                "carreras": carrera,
                "generos": genero,
            },
        )

    def retrieve_material(self, request, material_pk=None):
        material = Material.objects.get(pk=material_pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    def ejemplares(self, request, material_pk=None):
        ejemplar = Ejemplar.objects.filter(material=material_pk)
        serializer = EjemplarSerializer(ejemplar, many=True)
        return render(
            request,
            "ejemplares/listar_ejemplares.html",
            {"ejemplares": serializer.data},
        )

    def detalle_material(self, request, material_pk=None):
        material = Material.objects.get(pk=material_pk)
        tipo = TipoMaterial.objects.all()
        editorial = Editorial.objects.all()
        autor = Autor.objects.all()
        carrera = Carrera.objects.all()
        genero = Genero.objects.all()
        serializer = MaterialSerializer(material)
        return render(
            request,
            "materiales/detalle_material.html",
            {
                "material": serializer.data,
                "tipos": tipo,
                "editoriales": editorial,
                "autores": autor,
                "carreras": carrera,
                "generos": genero,
            },
        )

    def crear_material(self, request):
        if request.method == "POST":

            autores_data = request.POST.getlist("autores", [])
            tipo_data = request.POST.get("tipo", "")
            editorial_data = request.POST.get("editorial", "")
            carrera_data = request.POST.get("carrera", "")
            genero_data = request.POST.get("genero", "")

            data = request.POST.copy()
            data.pop("autores", None)
            data.pop("tipo", None)
            data.pop("editorial", None)
            data.pop("carrera", None)
            data.pop("genero", None)

            serializer = MaterialSerializer(data=data)
            if serializer.is_valid():
                material = serializer.save()

                for autor_name in autores_data:
                    nombre_apellido = autor_name.split()
                    if len(nombre_apellido) == 1:
                        nombre = nombre_apellido
                        autor, created = Autor.objects.get_or_create(
                            nombre=nombre, apellido=""
                        )
                        material.autor.add(autor)
                    elif len(nombre_apellido) > 1:
                        nombre, apellido = nombre_apellido
                        autor, created = Autor.objects.get_or_create(
                            nombre=nombre, apellido=apellido
                        )
                        material.autor.add(autor)
                    else:
                        continue

                if tipo_data:
                    tipo, created = TipoMaterial.objects.get_or_create(nombre=tipo_data)
                    material.tipo.add(tipo)

                if editorial_data:
                    editorial, created = Editorial.objects.get_or_create(
                        nombre=editorial_data
                    )
                    material.editorial.add(editorial)

                if carrera_data:
                    carrera, created = Carrera.objects.get_or_create(
                        nombre=carrera_data
                    )
                    material.carrera.add(carrera)

                if genero_data:
                    genero, created = Genero.objects.get_or_create(nombre=genero_data)
                    material.genero.add(genero)

                message = "Material creado exitosamente. "
                return JsonResponse(
                    {
                        "success": True,
                        "message": message,
                    }
                )

            error_messages = [
                f"{field}: {error[0]}" for field, error in serializer.errors.items()
            ]
            return JsonResponse({"success": False, "message": error_messages})

    def update_material(self, request, material_pk=None):
        try:
            material = Material.objects.get(pk=material_pk)
        except Material.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Material no encontrado."}
            )

        autores_data = request.POST.getlist("autores", [])
        tipo_data = request.POST.get("tipo", "")
        editorial_data = request.POST.get("editorial", "")
        carrera_data = request.POST.get("carrera", "")
        genero_data = request.POST.get("genero", "")

        """ for autor_name in autores_data:
            if len(autor_name.split()) <= 1:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "El autor debe contener al menos un Nombre y un Apellido.",
                    }
                ) """

        data = request.POST.copy()
        data.pop("autores", None)
        data.pop("tipo", None)
        data.pop("editorial", None)
        data.pop("carrera", None)
        data.pop("genero", None)

        serializer = MaterialSerializer(material, data=data, partial=True)
        if serializer.is_valid():
            material = serializer.save()

            # Limpiar relaciones existentes y añadir las nuevas
            material.autor.clear()
            for autor_name in autores_data:
                nombre_apellido = autor_name.split()

                if len(nombre_apellido) == 1:
                    nombre = nombre_apellido
                    autor, created = Autor.objects.get_or_create(
                        nombre=nombre, apellido=""
                    )
                    material.autor.add(autor)
                elif len(nombre_apellido) > 1:
                    nombre, apellido = nombre_apellido
                    autor, created = Autor.objects.get_or_create(
                        nombre=nombre, apellido=apellido
                    )
                    material.autor.add(autor)
                else:
                    continue

            if tipo_data:
                tipo, created = TipoMaterial.objects.get_or_create(nombre=tipo_data)
                material.tipo.set([tipo])

            if editorial_data:
                editorial, created = Editorial.objects.get_or_create(
                    nombre=editorial_data
                )
                material.editorial.set([editorial])

            if carrera_data:
                carrera, created = Carrera.objects.get_or_create(nombre=carrera_data)
                material.carrera.set([carrera])

            if genero_data:
                genero, created = Genero.objects.get_or_create(nombre=genero_data)
                material.genero.set([genero])

            return JsonResponse(
                {"success": True, "message": "Material actualizado exitosamente."}
            )

        error_messages = [
            f"{field}: {error[0]}" for field, error in serializer.errors.items()
        ]
        return JsonResponse({"success": False, "message": error_messages})

    def generar_pdf_material(request, material_pk):
        material = get_object_or_404(Material, pk=material_pk)
        response = HttpResponse(content_type="application/pdf")
        response["content-Disposition"] = (
            f'attachment; filename="material_{material_pk}.pdf"'
        )

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 100, f"ID del Material: {material.id}")

        p.drawString(100, height - 120, f"Titulo: {material.titulo}")

        p.drawString(100, height - 140, "Autor:")
        y = height - 160
        for autor in material.autor.all():
            p.drawString(120, y, f"{autor.nombre} {autor.apellido}")
            y -= 20

        p.drawString(100, y, "Tipo:")
        y -= 20
        for tipo in material.tipo.all():
            p.drawString(120, y, tipo.nombre)
            y -= 20

        p.drawString(100, y, "Genero:")
        y -= 20
        for genero in material.genero.all():
            p.drawString(120, y, genero.nombre)
            y -= 20

        p.drawString(100, y, "Editorial:")
        y -= 20
        for editorial in material.editorial.all():
            p.drawString(120, y, editorial.nombre)
            y -= 20

        p.drawString(100, y, "Carrera:")
        y -= 20
        for carrera in material.carrera.all():
            p.drawString(120, y, carrera.nombre)
            y -= 20

        p.drawString(100, y, f"Descripción: {material.descripcion}")
        y -= 20
        p.drawString(100, y, f"Estado: {material.estado}")

        p.showPage()
        p.save()

        return response


class EjemplarViewSet(viewsets.ModelViewSet):
    serializer_class = EjemplarSerializer
    queryset = Ejemplar.objects.all()

    def list(self, request, *args, **kwargs):
        material = Material.objects.all()
        query = request.GET.get("query", "")
        if query:
            ejemplares = Ejemplar.objects.filter(
                Q(id__icontains=query)
                | Q(material__titulo__icontains=query)
                | Q(material__autor__nombre__icontains=query)
                | Q(material__descripcion__icontains=query)
            ).distinct()
        else:
            ejemplares = Ejemplar.objects.all()

        paginator = Paginator(ejemplares, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ejemplares_serializer = EjemplarSerializer(page_obj, many=True)
        serializer_ejemplares = ejemplares_serializer.data
        return render(
            request,
            "ejemplares/listar_ejemplares.html",
            {
                "page_obj": page_obj,
                "query": query,
                "ejemplares": serializer_ejemplares,
                "materiales": material,
            },
        )

    def crear_ejemplar(self, request):
        if request.method == "POST":
            material_data = request.POST.get("material", "")
            data = request.data.copy()
            serializer = EjemplarSerializer(data=data)
            if serializer.is_valid():
                try:
                    material = Material.objects.get(titulo=material_data)
                    ejemplar = Ejemplar.objects.create(material=material)
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Ejemplar creado exitosamente.",
                            "ejemplarID": ejemplar.id,
                        }
                    )
                except Material.DoesNotExist:
                    return JsonResponse(
                        {
                            "status": 404,
                            "success": False,
                            "message": "El material ingresado no existe. \n¿Desea crearlo?",
                        }
                    )
            error_messages = [
                f"{field}: {error[0]}" for field, error in serializer.errors.items()
            ]
            return JsonResponse({"success": False, "message": error_messages})


def index(request):
    return render(request, "../templates/navbar.html")
