from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        acc_data = sociallogin.serialize().get("account", {})
        extra_data = acc_data.get("extra_data", {})
        image = extra_data.get("picture", None)
        if image:
            user.image = image

        return user
