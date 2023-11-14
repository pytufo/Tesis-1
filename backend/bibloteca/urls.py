from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("materiales.urls")),
    path("account/", include("accounts.urls")),
    path("api/reservas/", include("reservas.urls")),
    # path('api/Articulo/<int:pk>', views.DetailArticuloView.as_view())
]
