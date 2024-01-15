# from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", include("materiales.urls")),
    # path("api/", include("reservas.urls")),
    path("auth/", include("accounts.urls")),
    # path("admin/", include("dashboard.urls")),
    path("movimientos/", include("reservas.urls")),
]
