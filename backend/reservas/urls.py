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
        "reservas/usr/",
        ReservaViewSet.as_view(
            {
                "get": "listar_reservas_usuario",
            }
        ),
        name="entrega_reserva",
    ),
    path(
        "prestamo/<int:pk>/devolucion/",
        PrestamoViewSet.as_view(
            {
                "put": "devolucion",
            }
        ),
        name="prestamo-devolucion",
    ),
    path(
        "reservas/<int:pk>/cancelar/",
        ReservaViewSet.as_view(
            {
                "put": "cancelar_reserva",
            }
        ),
        name="prestamo-devolucion",
    ),
]
