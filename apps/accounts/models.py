"""The user model"""
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user class"""
    # TODO: add an id field
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.URLField(null=True, blank=True, default=settings.DEFAULT_AVATER_URL)

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
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}".strip()

    def get_short_name(self):
        """returns the short name for the user"""
        return self.first_name
    
    def send_mail(
            self, subject, body: str="", text_template=None, html_template=None,
            from_email: str | None=None, html_context={}, text_context={},
            ):
        """
        Send an email to the user, email notification, etc
        :params
            - subject: the subject of the email
            - body: the email body, optional if you are providing a text_template
            - text_template: a file path to the template file to render as the email message
            - html_template: a file path to the template file to render as the multipart email
            - from_email: the from email to use. default to `DEFAULT_FROM_EMAIL` in settings
            - html_context: the context dict to go with the html template
            - text_context: the context dict to go with the text template
        """
        if not subject:
            raise ValueError("Must include mail subject")
        if (not body and not text_template and not html_template):
            raise ValueError("Must set either the body text, text template or html template parameter")
        if body and text_template:
            raise ValueError("Can't use both body and text_template. Choose one based on your need, both are the same")
        if not body and not text_template:
            raise ValueError("Must set either body or text_template parameter")
        
        from_email = from_email if from_email else settings.DEFAULT_FROM_EMAIL
        if text_template:
            body = render_to_string(text_template, text_context)
        if html_template:
            html_template = render_to_string(html_template, html_context)

        return send_mail(subject,
                  body,
                  from_email,
                  [self.email],
                  fail_silently=settings.DEBUG, # fail silently in production
                  html_message=html_template,
                  )
    
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


class OTPModel(models.Model):
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp")

    def __str__(self):
        return f"OTP for user: {self.user.email}"

