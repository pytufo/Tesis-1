from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from datetime import timedelta


from materiales.utils import get_cantidad_disponible
from .models import Reserva, Prestamo


# Segun el resultado del seguimiento en "Materiales", establecemos un limite de reservas y prestamos para los usuarios.
# Hay que filtrar que el usuario no exeda un limite de reservas y prestamos
# Y por ultimo chequeamos que la el usuario no realize la misma reserva...


def get_reservas_prestamos_usuario(obj):
    reservas_usuario = Reserva.objects.filter(owner=obj.id)
    prestamos_usuario = Prestamo.objects.filter(owner=obj.id)

    cantidad_reservas = reservas_usuario.count()
    cantidad_prestamos = prestamos_usuario.count()

    movimientos = [
        {
            "id": reserva.id,
            "material": reserva.material.id,
            "fecha_inicio": reserva.fecha_inicio,
            "fecha_fin": reserva.fecha_fin,
            "estado": get_estado_reserva(reserva),
            "visto": reserva.visto,
            "tipo": "reserva",  # Identificador de tipo de movimiento
        }
        for reserva in reservas_usuario
    ] + [
        {
            "id": prestamo.id,
            "material": prestamo.ejemplar.material.id,
            "fecha_inicio": prestamo.fecha_inicio,
            "fecha_fin": prestamo.fecha_fin,
            "estado": get_estado_prestamo(prestamo),
            "visto": prestamo.visto,
            "tipo": "prestamo",  # Identificador de tipo de movimiento
        }
        for prestamo in prestamos_usuario
    ]

    movimientos_ordenados = sorted(movimientos, key=lambda x: x['fecha_inicio'])

    reservas_list = [
        {
            "id": reserva.id,
            "material": reserva.material.id,
            "fecha_inicio": reserva.fecha_inicio,
            "fecha_fin": reserva.fecha_fin,
            "estado": get_estado_reserva(reserva),
            "visto": reserva.visto,
        }
        for reserva in reservas_usuario
    ]
    prestamos_list = [
        {
            "id": prestamo.id,
            "material": prestamo.ejemplar.material,
            "fecha_inicio": prestamo.fecha_inicio,
            "fecha_fin": prestamo.fecha_fin,
            "estado": get_estado_prestamo(prestamo),
            "visto": prestamo.visto,
        }
        for prestamo in prestamos_usuario
    ]

    return {
        "cantidad_reservas": cantidad_reservas,
        "cantidad_prestamos": cantidad_prestamos,
        "reservas_usuario": reservas_list,
        "prestamos_usuario": prestamos_list,
        "movimientos": movimientos_ordenados,
    }


def get_limite_reservas_prestamo(obj):
    fecha_actual = timezone.now()
    limite = 4
    reservas = Reserva.objects.filter(owner=obj.id).filter(
        Q(fecha_fin__gte=fecha_actual) | Q(fecha_fin__isnull=True)
    )
    # get_reservas_prestamos_usuario(obj)["cantidad_reservas"]
    prestamos = Prestamo.objects.filter(owner=obj.id).filter(
        Q(fecha_fin__gte=fecha_actual) | Q(fecha_fin__isnull=True)
    )
    cantidad_reservas = reservas.count()
    cantidad_prestamos = prestamos.count()
    #get_reservas_prestamos_usuario(obj)["cantidad_prestamos"]

    if (cantidad_reservas + cantidad_prestamos) >= limite:
        return "Excede"
    else:
        return "Dispone"


def get_limite_epera(obj):
    limite = get_cantidad_disponible(obj)
    cantidad_disponible = limite
    return cantidad_disponible


def usuario_tiene_reserva_prestamo_pendiente(usuario, material):
    reservas_usuario = Reserva.objects.filter(owner=usuario, material=material)
    prestamos_usuario = Prestamo.objects.filter(
        owner=usuario, ejemplar__material=material
    )

    for reserva in reservas_usuario:
        estado_reserva = get_estado_reserva(reserva)
        if estado_reserva != "Finalizada":
            return {"tipo": "Reserva"}
    for prestamo in prestamos_usuario:
        estado_prestamo = get_estado_prestamo(prestamo)
        if estado_prestamo != "Finalizado":
            return {"tipo": "Prestamo"}


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
    elif reserva.fecha_fin is None:
        return "En lista de espera"
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


def get_reserva_lista_espera(material):
    try:
        reserva_lista_espera = (
            Reserva.objects.filter(material=material, fecha_fin__isnull=True)
            .order_by("fecha_inicio")
            .first()
        )
        return reserva_lista_espera
    except Reserva.DoesNotExist:
        return None


def habilitar_reserva_lista_espera(material, fecha_fin_anterior):
    reserva_lista_espera = get_reserva_lista_espera(material)

    if reserva_lista_espera:

        reserva_lista_espera.fecha_inicio = fecha_fin_anterior
        reserva_lista_espera.fecha_fin = timezone.now() + timedelta(days=1)
        reserva_lista_espera.save()
