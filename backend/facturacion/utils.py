from django.utils import timezone
from .models import Cuota
from accounts.models import User

def get_estado_cuota():
    # hay que definir el limite de fechas mensual de cuotas a 30 dias. 
    pass

def sancion():
    # tomamos los 3 ultimos pagos del usuario, si almenos 1 de esos pagos fue demorado; el limite de reservas para este usuario seria de 1
    pass