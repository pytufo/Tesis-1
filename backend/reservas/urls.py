from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  #

from .views import (
    ReservaViewSet,
    PrestamoViewSet,
    # create_fake,
)

router = DefaultRouter()
router.register(r"reservas", ReservaViewSet, basename="reserva")
# router.register(r"reserva/espera", PrestamoViewSet, basename="espera")
router.register(r"prestamo", PrestamoViewSet, basename="prestamo")

reserva_router = NestedDefaultRouter(router, r"reservas", lookup="reserva")
reserva_router.register(r"prestamo", PrestamoViewSet, basename="entregar-ejemplar")


urlpatterns = [
    path(r"", include(router.urls)),
    path(
        "reservas/<int:reserva_pk>",
        ReservaViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="detalle_reserva",
    ),
    path(
        "reserva/<int:reserva_pk>",
        ReservaViewSet.as_view(
            {
                "get": "detalle_reserva",
            }
        ),
        name="detalle_reserva",
    ),
    path(
        "reservas/<int:reserva_pk>/entregar_ejemplar/",
        PrestamoViewSet.as_view(
            {
                "get": "retrieve_reserva",
                "post": "entregar_ejemplar_reserva",
            }
        ),
        name="entrega_reserva",
    ),
    path(
        "reservas/",
        ReservaViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="listar_reservas",
    ),
    path(
        "mis_reservas/",
        ReservaViewSet.as_view(
            {
                "get": "listar_reservas_usuario",
            }
        ),
        name="reservas_usuario",
    ),
    path(
        "prestamos/",
        PrestamoViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="listar_prestamos",
    ),
    path(
        "prestamos/<int:pk>",
        PrestamoViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
        name="listar_prestamos",
    ),
    path(
        "prestamo/<int:prestamo_pk>",
        PrestamoViewSet.as_view(
            {
                "get": "detalle_prestamo",
            }
        ),
        name="detalle_prestamo",
    ),
    path(
        "mis_prestamos/",
        PrestamoViewSet.as_view(
            {
                "get": "listar_prestamos_usuario",
            }
        ),
        name="prestamos_usuario",
    ),
    path(
        "prestamos/nuevo/",
        PrestamoViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="nuevo_prestamo",
    ),
    path(
        "prestamo/<int:pk>/devolucion/",
        PrestamoViewSet.as_view(
            {
                "post": "devolucion",
            }
        ),
        name="prestamo_devolucion",
    ),
    path(
        "reservas/<int:pk>/cancelar/",
        ReservaViewSet.as_view(
            {
                "post": "cancelar_reserva",
            }
        ),
        name="cancelar_reserva",
    ),
]
