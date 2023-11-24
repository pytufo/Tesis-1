from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ReservaViewSet,
    PrestamoViewSet,
)

router = DefaultRouter()
router.register(r"reserva", ReservaViewSet, basename="reserva")
router.register(r"prestamo", PrestamoViewSet, basename="prestamo")

urlpatterns = [
    path(r"", include(router.urls)),
    # path("search/", views.ReservasSearchView.as_view(), name="reservas-search"),
]
