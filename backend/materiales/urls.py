from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
from reservas import views

# Creamos un enrutador para registrar los "ViewSets" ya que hasta ahora hay tambien vistas "generics".

router = DefaultRouter()
router.register(r"autor", AutorViewSet)
router.register(r"material", MaterialViewSet)
router.register(r"carrera", CarreraViewSet)
router.register(r"editorial", EditorialViewSet)
router.register(r"ejemplar", EjemplarViewSet)
router.register(r"genero", GeneroViewSet)
router.register(r"tipo", TipoMaterialViewSet)
urlpatterns = [
    path(r"material/", include(router.urls)),    
    path("movimientos/", include("reservas.urls")),
    path("generar/", generar_datos_aleatorios, name="generar"),
]
