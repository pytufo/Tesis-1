import django_filters
from .models import Prestamo, Reserva


class PrestamoFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="owner__username", lookup_expr="icontains"
    )
    email = django_filters.CharFilter(
        field_name="owner__email", lookup_expr="icontains"
    )

    titulo = django_filters.CharFilter(
        field_name="ejemplar__material__titulo", lookup_expr="icontains"
    )

    class Meta:
        model = Prestamo
        fields = ["username", "email", "titulo"]


class ReservaFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="owner__username", lookup_expr="icontains"
    )
    email = django_filters.CharFilter(
        field_name="owner__email", lookup_expr="icontains"
    )

    titulo = django_filters.CharFilter(
        field_name="material__titulo", lookup_expr="icontains"
    )

    class Meta:
        model = Prestamo
        fields = ["username", "email", "titulo"]
