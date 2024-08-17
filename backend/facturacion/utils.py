from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Cuota, Configuracion
from accounts.models import User


def es_moroso(user, fecha_limite=None):
    configuracion = Configuracion.objects.first()
    dias_tolerancia = configuracion.dias_tolerancia if configuracion else 30
    if fecha_limite is None:
        fecha_limite = timezone.now() - timedelta(days=dias_tolerancia)
    # fecha_limite = timezone.now() - timedelta(days=dias_tolerancia)
    cuotas_atrasadas = Cuota.objects.filter(owner=user, fecha__lt=fecha_limite)
    if cuotas_atrasadas:
        return "Adeuda"
    elif not cuotas_atrasadas:
        return "Pagó"
    return cuotas_atrasadas.exists()


def total_cuotas_atrasadas(user):
    fecha_limite = timezone.now() - timedelta(days=30)
    cuotas_atrasadas = Cuota.objects.filter(owner=user, fecha__lt=fecha_limite)
    total_cuotas = cuotas_atrasadas.aggregate(total=models.Sum("monto"))["total"] or 0
    return total_cuotas

##Si el usuario adeuda solamente 1 cuota podra reservar solo un material