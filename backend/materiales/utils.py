from materiales.models import Ejemplar
from reservas.models import Reserva, Prestamo, ListaEspera


# Definimos consultas para el seguimiento de los materiales (cantidades de prestamos, reservas, etc)
# Al final del seguimiento definimos un estado del material asignandole "Disponible", "Lectura", "No Disponible"


def get_cantidad_existente(obj):
    return Ejemplar.objects.filter(material=obj.id).count()


def get_cantidad_en_reserva(obj):
    return Reserva.objects.filter(material=obj.id).count()


def get_cantidad_en_prestamo(obj):
    return Prestamo.objects.filter(ejemplar=obj.id).count()


def get_cantidad_en_espera(obj):
    return ListaEspera.objects.filter(material=obj.id).count()


def get_cantidad_disponible(obj):
    cantidad_existente = get_cantidad_existente(obj)
    cantidad_en_reserva = get_cantidad_en_reserva(obj)
    cantidad_en_prestamo = get_cantidad_en_prestamo(obj)
    cantidad_disponible = cantidad_existente - (
        cantidad_en_reserva + cantidad_en_prestamo
    )
    return cantidad_disponible


def get_estado(obj):
    cantidad_disponible = get_cantidad_disponible(obj)
    if cantidad_disponible > 1:
        return "Disponible"
    elif cantidad_disponible == 1:
        return "Lectura"
    else:
        return "No Disponible"
