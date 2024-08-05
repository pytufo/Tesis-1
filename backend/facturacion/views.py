from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from datetime import timedelta
from django.utils import timezone

from rest_framework import viewsets, status

from accounts.serializers import UserProfileSerializer
from .serializers import CuotaSerializer, CuotaCreateSerializer

from .models import Cuota
from accounts.models import User


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

    def retrieve(self, request, pk=None):
        cuota = self.get_object()
        serializer = CuotaSerializer(cuota)
        return JsonResponse(serializer.data)

    def create(self, request):
        owner_email = request.data.get("owner")
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

        serializer = CuotaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(
            {"status": "success", "message": "Pago efectuado con éxito"},
            status=status.HTTP_201_CREATED,
        )
