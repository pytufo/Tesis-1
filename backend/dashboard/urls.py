from django.urls import path
from . import views

# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [ 
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
]