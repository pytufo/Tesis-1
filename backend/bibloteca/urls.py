# from django.contrib import admin
from django.urls import path, include
from materiales.views import MaterialViewSet, index
from django.http import Http404
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "err/404.html", {})

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(
        "",
        MaterialViewSet.as_view({"get": "listar_materiales"}),
        name="listar_materiales",
    ),
    path("material/", include("materiales.urls")),
    # path("api/", include("reservas.urls")),
    path("accounts/", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # path("admin/", include("dashboard.urls")),
    path("movimientos/", include("reservas.urls")),
    path("facturacion/", include("facturacion.urls")),
    path("error", custom_404, name='404')
    
] 
