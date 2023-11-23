from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from .serializers import DetalleUserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from accounts.models import User


class UserDetailView(RetrieveUpdateDestroyAPIView):
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
        super(UserDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {
            "status": status.HTTP_200_OK,
            "message": "Successfully updated",
            "result": data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(UserDetailView, self).delete(request, args, kwargs)
        response = {"status": status.HTTP_200_OK, "message": "Successfully deleted"}
        return Response(response)


"""
class UserListView(generics.ListAPIView):
    # Gestion de usuarios para el administrador

    serializer_class = UserListSerializer
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
 """
