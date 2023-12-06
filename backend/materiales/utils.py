from materiales.models import Articulo, Ejemplar


def get_cantidad_existente(obj):
    return Ejemplar.objects.filter(articulo=obj.id).count()


def get_cantidad_en_reserva(obj):
    from reservas.models import Reserva

    return Reserva.objects.filter(articulo=obj.id).count()


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
