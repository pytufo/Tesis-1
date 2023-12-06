from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserLoginView,
    LogoutView,
    RegisterView,
    generar_aleatorios,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="buscar")
urlpatterns = [
    path("", include(router.urls)),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="sign_up"),
    path("generar/", generar_aleatorios, name="generar_usuarios"),
]
