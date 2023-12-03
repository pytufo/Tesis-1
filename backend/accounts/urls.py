from django.urls import path
from .views import UserLoginView, LogoutView, RegisterView, generar_aleatorios, userView

urlpatterns = [
    path("", userView.as_view(), name="login"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="sign_up"),
    path("generar/", generar_aleatorios, name="generar_usuarios"),
]
