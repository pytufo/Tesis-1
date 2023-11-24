from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSuperuser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from .serializers import DetalleUserSerializer
from rest_framework import generics
from accounts.models import User


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSuperuser)
    queryset = User.objects.all()
    serializer_class = DetalleUserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully retrieved",
            "result": data,
        }
        return Response(response)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully updated",
            "result": data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        confirmation = request.data.get("confirm", False)
        if confirmation:
            self.perform_destroy(instance)
            response = {"status": status.HTTP_200_OK, "message": "Successfully deleted"}
            return Response(response)
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Comfirmation required",
            }
            return Response(response)


class UserListView(generics.ListAPIView):
    # Gestion de usuarios para el administrador

    serializer_class = DetalleUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "users": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
