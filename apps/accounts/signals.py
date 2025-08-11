from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from allauth.account.signals import email_confirmed

from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(email_confirmed)
def send_welcome_email(request, email_address, **kwargs):
    try:
        user = User.objects.get(email=email_address)
        user.send_mail(
            "Welcome to our app",
            f"""Hello {user.get_full_name()},\
            \nIts good to have you in our midst, feel at home.
            """,
        )
    except User.DoesNotExist:
        # TODO: log and fail silently
        pass
    except Exception as e:
        raise e
