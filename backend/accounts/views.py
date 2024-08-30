from faker import Faker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.db.models import Q

from django.shortcuts import render, redirect

fake = Faker()
import random

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsActive, IsSuperuser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status, generics, viewsets

from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response


from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from accounts.serializers import (
    UserProfileSerializer,
    CustomUserSerializer,
    UserLoginSerializer,
    RegisterSerializer,
)

from .models import User

#### Canales y notificacion
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@csrf_exempt
@require_POST
def generar_aleatorios(request):
    usuarios = []
    for _ in range(10):
        email = fake.email()
        # password = fake.last_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        role = fake.random_int(min=2, max=6)
        is_active = fake.boolean()
        is_staff = fake.boolean()

        numeros_aleatorios = "".join([str(random.randint(0, 9)) for _ in range(4)])
        password = f"{last_name}{numeros_aleatorios}"

        user = User.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=is_active,
            is_staff=is_staff,
        )
        usuarios.append(
            {
                "email": email,
                "password": password,
            }
        )

    return JsonResponse(
        {"message": "Usuarios aleatorios generados exitosamente", "usuarios": usuarios}
    )


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            owner = serializer.validated_data["owner"]
            login(request, owner)
            return redirect("/")
        else:
            error_message = "Usuario o contraseña inválidos"
            return render(
                request, "accounts/login.html", {"error_message": error_message}
            )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "accounts/login.html")


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")
        return Response(
            {"message": "Sesion cerrada exitosamente."}, status=status.HTTP_200_OK
        )

    """ def post(self, request, *args, **kwargs):
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
            ) """


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "auth/register.html")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            error_message = "Usuario registrado correctamente"
            return render(
                request,
                "auth/register.html",
                {"error_message": error_message, "status": 200},
            )
        else:
            error_message = [
                f"{field}: {error[0]}" for field, error in serializer.errors.items()
            ]
            return render(
                request,
                "auth/register.html",
                {"error_message": error_message, "status": 400},
            )


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=["post"])
    def editar_usuario(self, request, pk=None):
        usuario = get_object_or_404(User, pk=pk)
        role = request.POST.get("role")
        if role:
            usuario.role = role
            usuario.is_active = True
            usuario.save()
            return redirect("detalle_usuario", pk=usuario.id)
        return redirect("detalle_usuario", pk=usuario.id)

    def retrieve_user(self, request, *args, **kwargs):
        usuario = self.get_object()
        if (
            request.user.role == User.ADMIN
            or request.user.role == 2
            or request.user.role == 4
        ):
            serializer = CustomUserSerializer(usuario)
            roles = [
                role
                for role in User._meta.get_field("role").choices
                if role[0] != User.ADMIN
            ]
            return render(
                request,
                "accounts/detalle_usuario.html",
                {"usuario": serializer.data, "roles": roles},
            )
        else:
            return redirect("/")

    def listar_usuarios(self, request, *args, **kwargs):
        if request.user.role == 1 or request.user.role == 2 or request.user.role == 4:
            query = request.GET.get("query", "")
            ordering = request.GET.get("ordering", "id")
            if query:
                usuarios = User.objects.filter(
                    Q(email__icontains=query)
                    | Q(first_name__icontains=query)
                    | Q(dni__icontains=query)
                    | Q(last_name__icontains=query)
                ).exclude(Q(email="admin@mail.com") | Q(email=request.user.email))
            else:
                usuarios = User.objects.exclude(
                    (Q(email="admin@mail.com") | Q(email=request.user.email))
                )

            usuarios = usuarios.order_by(ordering)

            paginator = Paginator(usuarios, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            user_serializer = CustomUserSerializer(page_obj, many=True)
            serializer_user = user_serializer.data
            (page_number)
            return render(
                request,
                "accounts/listUsers.html",
                {
                    "usuarios": serializer_user,
                    "page_obj": page_obj,
                    "query": query,
                    "ordering": ordering,
                },
            )
        return redirect("/")

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def no_admin(self, request, pk=None):
        # users = User.objects.exclude(role=User.ADMIN)
        users = User.objects.exclude(Q(email="admin@mail.com") | Q(email=request.user.email))
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    """ @action(detail=True, methods=["put"])
    def activar(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
         """

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return render(request, "accounts/profile.html", {"user": serializer.data})
        """ serializer = self.get_serializer(user)
        return Response(serializer.data) """


@csrf_protect
def activar(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect("listar_usuarios")
    return HttpResponseForbidden()



def send_user_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            'type': 'send_notification',
            'notification': message
        }
    )