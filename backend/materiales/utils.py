from materiales.models import Material, Ejemplar
from accounts.models import User
from reservas.models import Reserva, Prestamo


# Definimos consultas para el seguimiento de los materiales (cantidades de prestamos, reservas, etc)
# Al final del seguimiento definimos un estado del material asignandole "Disponible", "Lectura", "No Disponible"


def get_cantidad_existente(obj):
    return Ejemplar.objects.filter(material=obj.id).count()


def get_cantidad_en_reserva(obj):
    return Reserva.objects.filter(material=obj.id).count()


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


# Segun el resultado del seguimiento, establecemos un limite de reservas y prestamos para los usuarios.
# Hay que filtrar que el usuario no exeda un limite de reservas y prestamos
# Y por ultimo chequeamos que la el usuario no realize la misma reserva...


def get_reservas_prestamos_usuario(obj):
    reservas_usuario = Reserva.objects.filter(owner=obj.id)
    prestamo_usuario = Prestamo.objects.filter(owner=obj.id)

    cantidad_reservas = reservas_usuario.count()
    cantidad_prestamos = prestamo_usuario.count()

    return cantidad_reservas, cantidad_prestamos


def get_limite_reservas_prestamo(obj):
    limite = 3
    cantidad_reservas = get_reservas_prestamos_usuario(obj)[0]
    cantidad_prestamos = get_reservas_prestamos_usuario(obj)[1]

    if (cantidad_reservas + cantidad_prestamos) >= limite:
        return "Excede"
    else:
        return "Dispone"


def usuario_tiene_reserva_pendiente(usuario, material):
    return Reserva.objects.filter(owner=usuario, material=material).exists()
