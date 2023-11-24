# from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),    
    path("api/", include("materiales.urls")),
    path("auth/", include("accounts.urls")),
    #path("api/reservas/", include("reservas.urls")),    
]
