from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout

from rest_framework.generics import GenericAPIView
from rest_framework import status, generics
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import render
from django.http import JsonResponse

from accounts.serializers import (
    UserLoginSerializer,
    RegisterSerializer,
    UserListSerializer,
    ProfileSerializer
)

from .models import User


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = serializer.is_valid(raise_exception=True)

        if user:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'access_token': serializer.data['access'],
                'refresh_token': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                }

            }
            return Response(response, status_code)
        return Response(status=status.HTTP_404_NOT_FOUND,)


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'sesion cerrada exitosamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""     def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'status_code': status_code,
                'access_token': serializer.data['access'],
                'refresh_token': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                }
            }

            return Response(response, status_code)
 """


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        super(UserDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully retrieved",
            "result": data
        }
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(UserDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully updated",
            "result": data
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(UserDetailView, self).delete(request, args, kwargs)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully deleted"
        }
        return Response(response)


class UserListView(generics.ListAPIView):
    # Gestion de usuarios para el administrador

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.is_superuser != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'El usuario no tiene los privilegios para esta accion.'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'users': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)


'''
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    #Testeamos el Logeo de usuario para verificar su Rol.
    if request.method == 'GET':
        if request.user.is_superuser:
            data = f"Congratulation {request.user.is_superuser},Admin your API just responded to GET request"            
            return Response({'response': data}, status=status.HTTP_200_OK)
            
        else:      
            data = request.user.role      
            return Response({'response': data}, status=status.HTTP_200_OK)
            
            
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token/',
        '/register/',
        '/token/refresh',
    ]
    return Response(routes)
'''
