from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserLoginView,
    LogoutView,
    RegisterView,
    generar_aleatorios,
    UserViewSet,
    activar
)

user_detail = UserViewSet.as_view({
    'get': 'retrieve_user'
})

urlpatterns = [
    
    path('<int:pk>/editar/', UserViewSet.as_view({'post': 'editar_usuario'}), name='editar_usuario'),
    path(
        "",
        UserViewSet.as_view(
            {
                "get": "listar_usuarios",
            }
        ),
        name="listar_usuarios",
    ),
    path(
        "users/",
        UserViewSet.as_view(
            {
                "get": "no_admin",
            }
        ),
        name="listar_usuarios_no_admin",
    ),
    path(
        "<int:pk>/",
        user_detail,
        name="detalle_usuario",
    ), 
    path('activar/', activar, name='activar'),
    path(
        "profile/",
        UserViewSet.as_view(
            {
                "get": "profile",
            }
        ),
        name="perfil",
    ),   
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("generar/", generar_aleatorios, name="generar_usuarios"),
]
