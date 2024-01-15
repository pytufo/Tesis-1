from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  #

from .views import (    
    PrestamoFilter,
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
        "reservas/<int:pk>/entrega_reserva/",
        ReservaViewSet.as_view(
            {"get": "retrieve_material", "post": "create_prestamo_de_reserva"}
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
    # path("reservas/<int:reserva_pk>/", {"get":})
    # path("buscar/", ArticuloFilter.as_view(), name="ejemplar_search"),
    # path("generar/", create_fake, name="generate fake data")
    # path("search/", views.ReservasSearchView.as_view(), name="reservas-search"),
]
