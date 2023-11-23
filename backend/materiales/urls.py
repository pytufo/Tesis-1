from django.urls import path
from . import views

urlpatterns = [
    path("articulo/", views.ListArticuloView.as_view(), name="List_Articulos"),
    path(
        "articulo/create/", views.CreateArticuloView.as_view(), name="Create_Articulo"
    ),
    path(
        "articulo/<int:pk>/", views.DetailArticuloView.as_view(), name="Articulo_detail"
    ),
    path("ejemplar/", views.ListEjemplarView.as_view(), name="List_Ejemplar"),
    path(
        "ejemplar/create/", views.CreateEjemplarView.as_view(), name="Create_Ejemplar"
    ),
    path(
        "ejemplar/<int:pk>/", views.DetailEjemplarView.as_view(), name="Ejemplar_detail"
    ),
]
