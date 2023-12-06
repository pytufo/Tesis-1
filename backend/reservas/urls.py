from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ReservaViewSet,
    PrestamoViewSet,
    ArticuloFilter,
    # create_fake,
)

router = DefaultRouter()
router.register(r"reserva", ReservaViewSet, basename="reserva")
router.register(r"prestamo", PrestamoViewSet, basename="prestamo")
router.register(r"buscar", ArticuloFilter, basename="buscar")

urlpatterns = [
    path(r"", include(router.urls)),
    #path("buscar/", ArticuloFilter.as_view(), name="ejemplar_search"),
    # path("generar/", create_fake, name="generate fake data")
    # path("search/", views.ReservasSearchView.as_view(), name="reservas-search"),
]
