import requests
from urllib.parse import urljoin
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
            self,
            request,
            custumer_key,
            custumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            _scope,
            scope_delimiter=" ",
            headers=None,
            basic_auth=False,
    ):
        super().__init__(
            request,
            custumer_key,
            custumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = CustomGoogleOAuth2Client


# 'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=782621328736-o4u0j11en1kq47t08edirf5f72l9h8sm.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline'

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        you can put this on the frontend. 
        you can have multiple callback url for different frontend view.
        the call back url will be called by Google based on the one that
        is passed in the google link parameter and must be registered on the
        Google console.
        """
        code = request.GET.get("code")
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: url should be replaced with the host base url
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})
        if response.status_code not in [200, 201]:
            response.raise_for_status() # TODO: implement this properly for a REST response

        return Response(response.json(), status=status.HTTP_200_OK)
