from django.utils import timezone
from materiales.utils import get_cantidad_en_espera, get_cantidad_disponible
from .models import Reserva, Prestamo

# Segun el resultado del seguimiento en "Materiales", establecemos un limite de reservas y prestamos para los usuarios.
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


def get_limite_epera(obj):
    limite = get_cantidad_disponible(obj)
    cantidad_espera = get_cantidad_en_espera(obj)
    cantidad_disponible = limite - cantidad_espera
    return cantidad_disponible


def usuario_tiene_reserva_pendiente(usuario, material):
    return Reserva.objects.filter(owner=usuario, material=material).exists()


# Definimos la logica para la "lista de espera".


def get_reserva_proxima_a_espirar(material):
    fecha_actual = timezone.now()

    reservas = Reserva.objects.filter(
        material=material, fecha_fin__gte=fecha_actual
    ).order_by("-fecha_fin")

    reserva_proxima = reservas.first() if reservas.exists() else None

    return reserva_proxima
