from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import CuotaViewSet, generar_pdf_cuota, GestionarCuotaViewSet

router = DefaultRouter()
router.register(r"cuotas", CuotaViewSet, basename="cuota")

urlpatterns = [
    # path(r"", include(router.urls)),
    path(
        "cuotas/", CuotaViewSet.as_view({"get": "listar_cuotas"}), name="listar_cuotas"
    ),
    path(
        "<int:pk>/",
        CuotaViewSet.as_view({"get": "detalle_cuota"}),
        name="detalle_cuota",
    ),
    path(
        "<int:cuota_pk>/comprobante/",
        generar_pdf_cuota,
        name="imprimir_comprobante",
    ),
    path(
        "gestionar/",
        GestionarCuotaViewSet.as_view({"get": "listar", "post": "update_configuracion"}),
        name="gestion_cuotas",
    ),
    path(
        "gestionar/data/",
        GestionarCuotaViewSet.as_view({"get": "list"}),
        name="gestion_cuotas_data",
    ),    
    path("nueva/", CuotaViewSet.as_view({"post": "create"}), name="nuevo_pago_cuota"),
]
