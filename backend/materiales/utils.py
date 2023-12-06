from materiales.models import Articulo, Ejemplar
from accounts.models import User
from reservas.models import Reserva, Prestamo


def get_cantidad_existente(obj):
    return Ejemplar.objects.filter(articulo=obj.id).count()


def get_cantidad_en_reserva(obj):
    return Reserva.objects.filter(articulo=obj.id).count()


def get_validar_limite_reservas(obj):
    reservas_usuario = Reserva.objects.filter(owner=obj.id)
    prestamo_usuario = Prestamo.objects.filter(owner=obj.id)

    cantidad_reservas = reservas_usuario.count()
    cantidad_prestamos = prestamo_usuario.count()

    return cantidad_reservas, cantidad_prestamos


def get_cantidad_disponible(obj):
    cantidad_existente = get_cantidad_existente(obj)
    cantidad_en_reserva = get_cantidad_en_reserva(obj)
    cantidad_disponible = cantidad_existente - cantidad_en_reserva
    return cantidad_disponible


def get_estado(obj):
    cantidad_disponible = get_cantidad_disponible(obj)
    if cantidad_disponible > 1:
        return "Disponible"
    elif cantidad_disponible == 1:
        return "Lectura"
    else:
        return "No Disponible"
