from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

fake = Faker()

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsActive
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from rest_framework.response import Response


from rest_framework_simplejwt.tokens import RefreshToken


from accounts.serializers import (
    userSerializer,
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
                "authenticatedUser": {
                    "email": user.email,
                    "role": user.role,
                },
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"success": False, "message": "Credenciales invalidas."},
            status=status.HTTP_404_NOT_FOUND,
        )


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "sesion cerrada exitosamente."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class userView(generics.ListAPIView):
    serializer_class = userSerializer
    queryset = User.objects.all()

