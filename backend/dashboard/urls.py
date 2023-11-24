from django.urls import path
from . import views

# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
]
