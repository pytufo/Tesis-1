from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter

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
)
from reservas.views import ReservaViewSet, ListaDeEsperaviewset, PrestamoViewSet


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

urlpatterns = [
    path(r"", include(router.urls)),
    path(
        "material/<int:material_pk>/ejemplares/",
        MaterialViewSet.as_view(
            {
                "get": "retrieve_material",
            }
        ),
    ),
    path(
        "ejemplar/<int:ejemplar_pk>/prestar/",
        PrestamoViewSet.as_view({"get": "retrieve_ejemplar", "post": "create"}),
    ),
    path(
        "material/<int:material_pk>/reservar/",
        ReservaViewSet.as_view({"get": "retrieve_material", "post": "create"}),
        name="reservar-material",
    ),
    path(
        "material/<int:material_pk>/reservar/espera/",
        ListaDeEsperaviewset.as_view({"get": "retrieve", "post": "create"}),
        name="espera-material",
    ),
    path("generar/", generar_datos_aleatorios, name="generar"),
    # path("movimientos/", include("reservas.urls")),
]
