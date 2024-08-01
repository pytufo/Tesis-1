from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from django.conf.urls import handler404


# from . import views
from .views import (
    AutorViewSet,
    MaterialViewSet,
    CarreraViewSet,
    EditorialViewSet,
    EjemplarViewSet,
    GeneroViewSet,
    TipoMaterialViewSet,
    generar_datos_aleatorios,
    generar_pdf_material,
)
from reservas.views import ReservaViewSet, PrestamoViewSet


# Creamos un enrutador para registrar los "ViewSets" ya que hasta ahora hay tambien vistas "generics".

router = DefaultRouter()
router.register(r"material", MaterialViewSet)
router.register(r"autor", AutorViewSet)
router.register(r"carrera", CarreraViewSet)
router.register(r"editorial", EditorialViewSet)
router.register(r"ejemplar", EjemplarViewSet)
router.register(r"genero", GeneroViewSet)
router.register(r"tipo", TipoMaterialViewSet)


material_router = NestedDefaultRouter(router, r"material", lookup="material")
material_router.register(r"reserva", ReservaViewSet, basename="reservar-material")
material_router.register(r"prestar", PrestamoViewSet, basename="prestar-ejemplar")
# material_router.register(r"autor", AutorViewSet, basename="material-autor")

# material_router.register(r"autor",)

material_detail = MaterialViewSet.as_view(
    {
        "get": "retrieve_material",
    }
)

urlpatterns = [
    # path(r"", include(router.urls)),
    path(
        "<int:material_pk>/",
        MaterialViewSet.as_view({"get": "detalle_material"}),
        name="material",
    ),
    path("<int:material_pk>/detail", material_detail, name="detalle_material"),
    path(
        "<int:material_pk>/editar_material",
        MaterialViewSet.as_view({"post": "update_material", "get": "detalle_material"}),
        name="editar_material",
    ),
    path(
        "nuevo/",
        MaterialViewSet.as_view({"post": "crear_material", "get": "listar_materiales"}),
        name="crear_material",
    ),
    path(
        "<int:material_pk>/pdf/",
        generar_pdf_material,
        name="generar_pdf_material",
    ),
    path(
        "<int:material_pk>/ejemplares/",
        MaterialViewSet.as_view(
            {
                "get": "ejemplares",
            }
        ),
        name="ejemplares_de_material",
    ),
    path(
        "ejemplares/",
        EjemplarViewSet.as_view({"get": "list"}),
        name="listar_ejemplares",
    ),
    path(
        "ejemplar/nuevo/",
        EjemplarViewSet.as_view({"post": "crear_ejemplar"}),
        name="crear_ejemplar",
    ),
    path(
        "ejemplar/<int:ejemplar_pk>/prestar/",
        PrestamoViewSet.as_view({"get": "retrieve_ejemplar", "post": "create"}),
        name="crear_prestamo",  
    ),
    path(
        "<int:material_pk>/reservar/",
        ReservaViewSet.as_view({"get": "retrieve_material", "post": "create"}),
        name="reservar_material",
    ),
    path("generar/", generar_datos_aleatorios, name="generar"),
    # path("movimientos/", include("reservas.urls")),
    # path("materiales/", MaterialViewSet.as_view({"get": "listar_materiales"}), name="listar_materiales"),
]
