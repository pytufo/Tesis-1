from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator


from datetime import timedelta
from django.utils import timezone

from rest_framework import viewsets, status

from accounts.serializers import UserProfileSerializer
from .serializers import CuotaSerializer, CuotaCreateSerializer

from .models import Cuota
from accounts.models import User

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


def generar_pdf_cuota(request, cuota_pk):
    cuota = get_object_or_404(Cuota, pk=cuota_pk)
    # damos formato mas legible a la fecha
    fecha = cuota.fecha.strftime(("%d/%m/%Y - %H:%M"))

    response = HttpResponse(content_type="application/pdf")
    response["content-Disposition"] = f'attachment; filename="cuota_{cuota_pk}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Trans. Nº: {cuota.id}")
    y = height - 120
    p.drawString(100, y, f"Motivo: Pago de membresia bibloteca UTN-Frcon ")
    y -= 20
    p.drawString(100, y, f"Fecha de emisión: {fecha}")
    y -= 20
    p.drawString(100, y, f"Cliente: ")
    y -= 20
    p.drawString(130, y, f"Id del cliente: {cuota.owner.id}")
    y -= 20
    p.drawString(130, y, f"Nombres: {cuota.owner.last_name}, {cuota.owner.first_name}")
    y -= 40
    p.drawString(400, y, f"Monto: ${cuota.monto}")
    y -= 20

    p.showPage()
    p.save()

    return response


class CuotaViewSet(viewsets.ModelViewSet):
    serializer_class = CuotaSerializer
    queryset = Cuota.objects.all()

    def list(self, request):
        cuota = Cuota.objects.all()
        serializer = CuotaSerializer(cuota, many=True)
        return JsonResponse(serializer.data, safe=False)

    def listar_cuotas(self, request):
        usuario = request.user
        query = request.GET.get("query", "")
        if usuario.role == 4 or usuario.role == 1:
            cuotas = Cuota.objects.all()
        else:
            return redirect("/")

        if query:
            cuotas = cuotas.filter(
                Q(owner__email__icontains=query)
                | Q(owner__first_name__icontains=query)
                | Q(owner__last_name__icontains=query)
            )

        paginator = Paginator(cuotas, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        cuotas_serializer = CuotaSerializer(page_obj, many=True)
        serializer_cuotas = cuotas_serializer.data

        # serializer = CuotaSerializer(cuota, many=True)
        return render(
            request,
            "facturacion/listar_cuotas.html",
            {"page_obj": page_obj, "cuotas": serializer_cuotas, "query": query},
        )

    def detalle_cuota(self, request, pk=None):
        cuota = self.get_object()
        serializer = CuotaSerializer(cuota)
        return render(
            request, "facturacion/detalle_cuota.html", {"cuota": serializer.data}
        )

    def retrieve(self, request, pk=None):
        cuota = self.get_object()
        serializer = CuotaSerializer(cuota)
        return JsonResponse(serializer.data)

    def create(self, request):
        owner_email = request.data.get("owner") or request.data.get("userID")
        fecha_default = timezone.now()
        monto = request.data.get("monto")

        try:
            owner = User.objects.get(email=owner_email)
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "El usuario a efectuar el pago no existe",
                }
            )
        data = {
            "created_by": request.user.id,
            "owner": owner.id,
            "monto": monto,
            "fecha": fecha_default,
        }

        serializer = CuotaCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(
            {"success": True, "message": "Pago efectuado con éxito"},
            status=status.HTTP_201_CREATED,
        )
