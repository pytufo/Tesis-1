from django.utils import timezone
from materiales.models import Ejemplar
from reservas.models import Reserva, Prestamo

# Definimos consultas para el seguimiento de los ejemplares (cantidades de prestamos, reservas, etc) y asignamos un estado segun el criterio del seguimiento. y tambien establecemos parametros de vencimiento en los prestamos.


def get_ejemplares_de_material(material):
    return Ejemplar.objects.filter(material=material)


def get_estado_ejemplar(obj):
    estado = "Disponible"

    prestamo = Prestamo.objects.filter(ejemplar=obj).order_by("-fecha_inicio").first()

    if prestamo:
        if prestamo.fecha_fin and prestamo.fecha_fin < timezone.now():
            estado = "Disponible"
        else:
            estado = "En prestamo"

    return estado


def get_ejemplares_disponibles(material):
    ejemplares = get_ejemplares_de_material(material)
    ejemplares_disponibles = []

    for ejemplar in ejemplares:
        if get_estado_ejemplar(ejemplar) == "Disponible":
            ejemplares_disponibles.append(ejemplar.id)

    return ejemplares_disponibles


# Definimos consultas para el seguimiento de los materiales (cantidades de prestamos, reservas, etc)
# Al final del seguimiento definimos un estado del material asignandole "Disponible", "Lectura", "No Disponible"


def get_cantidad_existente(obj):
    return Ejemplar.objects.filter(material=obj.id).count()


def get_cantidad_en_reserva(obj, vencidas=True):
    reservas = Reserva.objects.filter(material=obj.id)

    if vencidas:
        reservas = reservas.filter(fecha_fin__gte=timezone.now())

    return reservas.count()


def get_cantidad_en_prestamo(obj, vencidas=True):
    prestamos = Prestamo.objects.filter(ejemplar__material=obj.id)
    if vencidas:
        prestamos = prestamos.filter(fecha_fin__gte=timezone.now())

    return prestamos.count()


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
    cantidad_existente = get_cantidad_existente(obj)
    if cantidad_disponible > 1:
        return "Disponible"
    elif cantidad_disponible <= 1 and cantidad_existente > 1:
        # Verificar tambien la cantidad existente > 1
        return "Disponible (Lista de espera)"
    elif cantidad_disponible <= 1:
        return "No disponible (Solo lectura)"
