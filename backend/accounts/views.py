from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

fake = Faker()

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsActive, IsSuperuser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from accounts.serializers import (
    UserProfileSerializer,
    UserLoginSerializer,
    RegisterSerializer,
)

from .models import User


@csrf_exempt
@require_POST
def generar_aleatorios(request):
    for _ in range(10):
        User.objects.create(
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=fake.random_element(elements=(1, 2, 3, 4, 5, 6)),
            is_active=fake.boolean(),
            is_staff=fake.boolean(),
        )

    return JsonResponse({"message": "Usuarios aleatorios generados exitosamente"})


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                "success": True,
                "refresh_token": str(refresh),
                "access_token": str(access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"success": False, "message": "Credenciales invalidas."},
            status=status.HTTP_404_NOT_FOUND,
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            access_token = request.data.get("access_token")
            token = RefreshToken(access_token)
            token.blacklist()
            return Response(
                {"message": "Sesion cerrada exitosamente."}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Error al cerrar sesion: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperuser]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=["get"])
    def no_admin(self, request, pk=None):
        users = User.objects.exclude(role=User.ADMIN)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def activar(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


"""     def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        data = []
        for user in queryset:
            cantidad_reservas, cantidad_prestamos = get_reservas_prestamos_usuario(user)

            # Agrega la información al objeto user
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "cantidad_reservas": cantidad_reservas,
                "cantidad_prestamos": cantidad_prestamos,
            }

            data.append(user_data)

        return Response(data) """
