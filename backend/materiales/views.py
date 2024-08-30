from faker import Faker
import csv
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

from reservas.utils import get_reservas_prestamos_usuario
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


def export_materials_csv(request):
    # Crear la respuesta HTTP con el tipo de contenido para CSV
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="materials.csv"'

    writer = csv.writer(response)

    serializer = MaterialSerializer(Material.objects.all(), many=True)
    data = serializer.data

    # Cabeceras del csv
    header = [
        "ID",
        "Titulo",
        "Descripcion",
        "Tipo",
        "Editorial",
        "Autor",
        "Carrera",
        "Género",
        "Cantidad Existente",
    ]
    writer.writerow(header)
    for material in data:
        row = [
            material["id"],
            material["titulo"],
            material["descripcion"],
            ", ".join([tipo["nombre"] for tipo in material["tipo"]]),
            ", ".join([editorial["nombre"] for editorial in material["editorial"]]),
            ", ".join(
                [
                    f"{autor['nombre']} {autor['apellido']}"
                    for autor in material["autor"]
                ]
            ),
            ", ".join([carrera["nombre"] for carrera in material["carrera"]]),
            ", ".join([genero["nombre"] for genero in material["genero"]]),
            material["cantidad_existente"],
        ]
        writer.writerow(row)
    return response


def generar_pdf_materiales(request):
    # Crear la respuesta HTTP con el tipo de contenido para PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="materials.pdf"'

    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Serializar los datos
    serializer = MaterialSerializer(Material.objects.all(), many=True)
    data = serializer.data

    # Cabeceras del PDF
    header = [
        "ID",
        "Titulo",
        "Descripcion",
        "Tipo",
        "Editorial",
        "Autor",
        "Carrera",
        "Género",
        "Cantidad Existente",
    ]
    table_data = [header]

    # Filas del PDF
    for material in data:
        row = [
            material["id"],
            material["titulo"],
            material["descripcion"],
            ", ".join([tipo["nombre"] for tipo in material["tipo"]]),
            ", ".join([editorial["nombre"] for editorial in material["editorial"]]),
            ", ".join(
                [
                    f"{autor['nombre']} {autor['apellido']}"
                    for autor in material["autor"]
                ]
            ),
            ", ".join([carrera["nombre"] for carrera in material["carrera"]]),
            ", ".join([genero["nombre"] for genero in material["genero"]]),
            material["cantidad_existente"],
        ]
        table_data.append(row)

    # Crear la tabla
    table = Table(table_data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    # Añadir la tabla al PDF
    elements = [table]
    pdf.build(elements)

    # Obtener el contenido del buffer y devolverlo como respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response


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

    def listar_carreras(self, request):
        query = request.GET.get("query", "")
        carrera = Carrera.objects.all()

        if query:
            carreras = Carrera.objects.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query)
            ).distinct()
        else:
            carreras = Carrera.objects.all()

        paginator = Paginator(carreras, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        carrera_serializer = CarreraSerializer(page_obj, many=True)
        serializer_carrera = carrera_serializer.data

        return render(
            request,
            "materiales/carreras/listar_carreras.html",
            {
                "page_obj": page_obj,
                "query": query,
                "carreras": serializer_carrera,
            },
        )


class GeneroViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = GeneroSerializer
    queryset = Genero.objects.all()

    def listar_generos(self, request):
        query = request.GET.get("query", "")
        genero = Genero.objects.all()

        if query:
            generos = Genero.objects.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query)
            ).distinct()
        else:
            generos = Genero.objects.all()

        paginator = Paginator(generos, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        genero_serializer = GeneroSerializer(page_obj, many=True)
        serializer_genero = genero_serializer.data

        materiales = Material.objects.filter(genero__in=generos).distinct().count
        return render(
            request,
            "materiales/generos/listar_generos.html",
            {
                "page_obj": page_obj,
                "query": query,
                "generos": serializer_genero,
                "materiales": materiales,
            },
        )


class EditorialViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = EditorialSerializer
    queryset = Editorial.objects.all()

    def listar_editoriales(self, request):
        query = request.GET.get("query", "")
        editorial = Genero.objects.all()

        if query:
            editoriales = Editorial.objects.filter(
                Q(nombre__icontains=query)
            ).distinct()
        else:
            editoriales = Editorial.objects.all()

        paginator = Paginator(editoriales, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        editorial_serializer = EditorialSerializer(page_obj, many=True)
        serializer_editorial = editorial_serializer.data

        materiales = Material.objects.annotate(carrera_count=Count("carrera")).count()
        return render(
            request,
            "materiales/editoriales/listar_editoriales.html",
            {
                "page_obj": page_obj,
                "query": query,
                "editoriales": serializer_editorial,
                "materiales": materiales,
            },
        )


class TipoMaterialViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = TipoMaterialSerializer
    queryset = TipoMaterial.objects.all()

    def listar_tipo_material(self, request):
        query = request.GET.get("query", "")
        tipoMaterial = TipoMaterial.objects.all()

        if query:
            tipos = TipoMaterial.objects.filter(Q(nombre__icontains=query)).distinct()
        else:
            tipos = TipoMaterial.objects.all()

        paginator = Paginator(tipos, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        tipoMaterial_serializer = TipoMaterialSerializer(page_obj, many=True)
        serializer_tipoMaterial = tipoMaterial_serializer.data

        materiales = Material.objects.filter(tipo__in=tipos).distinct().count()
        return render(
            request,
            "materiales/tipos/listar_tipos.html",
            {
                "page_obj": page_obj,
                "query": query,
                "tipos": serializer_tipoMaterial,
                "materiales": materiales,
            },
        )


class AutorViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsSuperUserOrReadOnly,)
    """serializer_class = AutorSerializer
    queryset = Autor.objects.all()
    """
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()

    def listar_autores(self, request):
        query = request.GET.get("query", "")
        autor = Autor.objects.all()

        if query:
            autores = Autor.objects.filter(Q(nombre__icontains=query)).distinct()
        else:
            autores = Autor.objects.all()

        paginator = Paginator(autores, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        autor_serializer = AutorSerializer(page_obj, many=True)
        serializer_autor = autor_serializer.data

        return render(
            request,
            "materiales/autores/listar_autores.html",
            {
                "page_obj": page_obj,
                "query": query,
                "autores": serializer_autor,
            },
        )


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()

    def listar_materiales(self, request, *args, **kwargs):
        user = request.user
        query = request.GET.get("query", "")
        tipo = TipoMaterial.objects.all()
        editorial = Editorial.objects.all()
        autor = Autor.objects.all()
        carrera = Carrera.objects.all()
        genero = Genero.objects.all()
        ordering = request.GET.get("ordering", "")

        if query:
            materiales = Material.objects.filter(
                Q(titulo__icontains=query)
                | Q(autor__nombre__icontains=query)
                | Q(descripcion__icontains=query)
                | Q(editorial__nombre__icontains=query)
                | Q(tipo__nombre__icontains=query)
                | Q(genero__nombre__icontains=query)
            ).distinct()
        else:
            materiales = Material.objects.all()

        ####
        materials_serializer = MaterialSerializer(
            materiales, many=True, context={"user": user}
        )
        serializer_materials = materials_serializer.data

        if ordering == "-cantidad_existente":
            serializer_materials = sorted(
                serializer_materials, key=lambda x: x["cantidad_existente"]
            )
        elif ordering == "cantidad_existente":
            serializer_materials = sorted(
                serializer_materials,
                key=lambda x: x["cantidad_existente"],
                reverse=True,
            )
        elif ordering == "estado":
            serializer_materials = sorted(
                serializer_materials, key=lambda x: x["estado"]
            )
        elif ordering == "-estado":
            serializer_materials = sorted(
                serializer_materials, key=lambda x: x["estado"], reverse=True
            )
        else:
            if ordering:
                materiales = materiales.order_by(ordering)
                materials_serializer = MaterialSerializer(materiales, many=True)
                serializer_materials = materials_serializer.data

        paginator = Paginator(serializer_materials, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "materiales/listar_materiales.html",
            {
                "page_obj": page_obj,
                "query": query,
                "materials": page_obj.object_list,
                "materiales": materiales,
                "tipos": tipo,
                "editoriales": editorial,
                "autores": autor,
                "carreras": carrera,
                "generos": genero,
                "ordering": ordering,
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
        user = request.user
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
                "user": user,
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

            # verificar que no exista el material
            titulo = data.get("titulo", "").strip()
            tipos = TipoMaterial.objects.filter(nombre__in=tipo_data.split(","))

            if Material.objects.filter(titulo=titulo, tipo__in=tipos).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Ya existe un material con el mismo titulo y tipo.",
                    }
                )
            serializer = MaterialSerializer(data=data)
            if serializer.is_valid():
                material = serializer.save()

                for autor_name in autores_data:
                    nombre_apellido = autor_name.split()
                    if len(nombre_apellido) == 1:
                        nombre = nombre_apellido[0]
                        apellido = ""
                    elif len(nombre_apellido) > 1:
                        nombre, apellido = nombre_apellido
                    else:
                        continue
                    autor, created = Autor.objects.get_or_create(
                        nombre=nombre, apellido=apellido
                    )
                    material.autor.add(autor)

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
                    nombre = nombre_apellido[0]
                elif len(nombre_apellido) > 1:
                    nombre, apellido = nombre_apellido
                else:
                    continue
                autor, created = Autor.objects.get_or_create(
                    nombre=nombre, apellido=apellido
                )
                material.autor.add(autor)

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

    def retrieve_ejemplar(self, request, ejemplar_pk=None):
        ejemplar = Ejemplar.objects.get(pk=ejemplar_pk)
        serializer = EjemplarSerializer(ejemplar)
        return Response(serializer.data)

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
                            "message": "El material ingresado no existe.",
                        }
                    )
            error_messages = [
                f"{field}: {error[0]}" for field, error in serializer.errors.items()
            ]
            return JsonResponse({"success": False, "message": error_messages})


def index(request):
    return render(request, "../templates/navbar.html")
