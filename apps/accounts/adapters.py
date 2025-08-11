import random
from datetime import timedelta
from django.utils import timezone
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

from .models import OTPModel


class CustomSocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        acc_data = sociallogin.serialize().get("account", {})
        extra_data = acc_data.get("extra_data", {})
        image = extra_data.get("picture", None)
        if image:
            user.image = image

        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # TODO: use a better token generation library like pyotp
        code = str(random.randint(100000, 999999))
        OTPModel.objects.create(
            user=emailconfirmation.email_address.user,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=10)
        )
        ctx = {"code": code}
        template = 'accounts/email/email_confirmation_code'
        self.send_mail(template, emailconfirmation.email_address.email, ctx)
