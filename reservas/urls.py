from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservasView.as_view(), name='reservas'),
    path('search/', views.ReservasSearchView.as_view(), name='reservas-search'),
    path('Create/', views.ReservaCreateView.as_view(), name='reservas'),
    path('<int:pk>/', views.ReservaDetailView.as_view(), name='Reserva') 
]