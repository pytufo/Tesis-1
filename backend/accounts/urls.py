from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("login/refresh", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="sign_up"),
    path("users", views.UserListView.as_view(), name="users"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    # path('test/', views.testEndPoint, name='test')
]
