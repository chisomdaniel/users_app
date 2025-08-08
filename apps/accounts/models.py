"""The user model"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user class"""
    # TODO: add an id field
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        """meta class"""
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]

    def get_full_name(self):
        """returns the user first name and last name"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """returns the short name for the user"""
        return self.first_name
    
    def __str__(self):
        """return the str representation"""
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"[User Profile] {self.user.get_full_name()}"