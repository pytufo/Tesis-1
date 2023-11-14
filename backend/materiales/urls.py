from django.urls import path
from . import views

urlpatterns = [
    path('Titulo/', views.TituloView.as_view(), name='titulo'),
    path('Articulo/', views.ListArticuloView.as_view(), name='ListArticulos'),
    path('Articulo/create/', views.CreateArticuloView.as_view(),
         name='CreateArticulo'),
    path('Articulo/<int:pk>/', views.DetailArticuloView.as_view(), name='Articulo'),
    path('Ejemplar/', views.ListEjemplarView.as_view(), name='Ejemplar'),
    path('Ejemplar/Create/', views.CreateEjemplarView.as_view(), name='Ejemplar'),
    path('Ejemplar/<int:pk>/', views.DetailEjemplarView.as_view(), name='Ejemplar'),
]
