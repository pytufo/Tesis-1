from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from materiales import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("materiales.urls")),
    path("account/", include("accounts.urls")),
    path("api/reservas/", include("reservas.urls")),
    # path('api/Articulo/<int:pk>', views.DetailArticuloView.as_view())
]
