from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .admin_views import PrestamoViewSet, ReservaViewSet

app_name = "reservas"

router = DefaultRouter()
router.register(r"reserva", ReservaViewSet)
router.register(r"prestamo", PrestamoViewSet)

prestamo_router = NestedDefaultRouter(router, r"reserva", lookup="reserva")
prestamo_router.register(r"entrega", PrestamoViewSet, basename="entregar-material")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "reserva/<int:reserva_pk>/entregar/",
        PrestamoViewSet.as_view({"get": "retrieve", "post": "create"}),
    ),
]
