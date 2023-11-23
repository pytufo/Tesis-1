from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("role", 6)
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)        

        if extra_fields.get("is_superuser") != True:
            raise ValueError("Superuser must have role of Global Admin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # roles de usuario
    ADMIN = 1
    BIBLOTECARIO = 2
    PROFESOR = 3
    TESORERO = 4
    ALUMNO = 5
    INVITADO = 6

    role = (
        (ADMIN, "Administrador"),
        (BIBLOTECARIO, "Biblotecario"),
        (PROFESOR, "Profesor"),
        (TESORERO, "Tesorero"),
        (ALUMNO, "Alumno"),
        (INVITADO, "Invitado"),
    )

    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=role, blank=True, null=True, default=6
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class BlacklistToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
