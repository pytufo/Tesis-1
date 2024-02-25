from django.utils import timezone
from datetime import datetime


from materiales.utils import get_cantidad_en_espera, get_cantidad_disponible
from .models import Reserva, Prestamo

# Segun el resultado del seguimiento en "Materiales", establecemos un limite de reservas y prestamos para los usuarios.
# Hay que filtrar que el usuario no exeda un limite de reservas y prestamos
# Y por ultimo chequeamos que la el usuario no realize la misma reserva...


def get_reservas_prestamos_usuario(obj):
    reservas_usuario = Reserva.objects.filter(
        owner=obj.id, fecha_fin__gte=timezone.now()
    )
    prestamos_usuario = Prestamo.objects.filter(
        owner=obj.id, fecha_fin__gte=timezone.now()
    )

    cantidad_reservas = reservas_usuario.count()
    cantidad_prestamos = prestamos_usuario.count()

    reservas_list = [{'id': reserva.id, 'fecha_inicio': reserva.fecha_inicio, 'fecha_fin': reserva.fecha_fin} for reserva in reservas_usuario]
    prestamos_list = [{'id': prestamo.id, 'fecha_inicio': prestamo.fecha_inicio, 'fecha_fin': prestamo.fecha_fin} for prestamo in prestamos_usuario]

    return {
        'cantidad_reservas': cantidad_reservas,
        'cantidad_prestamos': cantidad_prestamos,
        'reservas_usuario': reservas_list,
        'prestamos_usuario': prestamos_list,
    }


def get_limite_reservas_prestamo(obj):
    limite = 4
    cantidad_reservas = get_reservas_prestamos_usuario(obj)['cantidad_reservas']
    cantidad_prestamos = get_reservas_prestamos_usuario(obj)['cantidad_prestamos']

    if (cantidad_reservas + cantidad_prestamos) >= limite:
        return "Excede"
    else:
        return "Dispone"


def get_limite_epera(obj):
    limite = get_cantidad_disponible(obj)
    cantidad_espera = get_cantidad_en_espera(obj)
    cantidad_disponible = limite - cantidad_espera
    return cantidad_disponible


def usuario_tiene_reserva_pendiente(usuario, material):
    reservas_usuario = Reserva.objects.filter(owner=usuario, material=material)

    for reserva in reservas_usuario:
        estado_reserva = get_estado_reserva(reserva)
        if estado_reserva != "Finalizada":
            return True
    return False


# Definimos la logica para la "lista de espera".


def get_reserva_proxima_a_espirar(material):
    fecha_actual = timezone.now()

    reservas = Reserva.objects.filter(
        material=material, fecha_fin__gte=fecha_actual
    ).order_by("-fecha_fin")

    reserva_proxima = reservas.first() if reservas.exists() else None

    return reserva_proxima


def get_estado_reserva(reserva):
    fecha_actual = timezone.now()
    if reserva.fecha_fin is not None and reserva.fecha_fin <= fecha_actual:
        return "Finalizada"
    elif reserva.fecha_fin is not None and reserva.fecha_fin > fecha_actual:
        return "En espera"
    else:
        return "Estado no definido"


def get_estado_prestamo(prestamo):
    fecha_actual = timezone.now()
    if prestamo.fecha_fin is not None and prestamo.fecha_fin <= fecha_actual:
        return "Finalizado"
    elif prestamo.fecha_fin is not None and prestamo.fecha_fin > fecha_actual:
        return "En prestamo"
    else:
        return "Estado no definido"
