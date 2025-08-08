"""accounts url"""
from django.urls import path, include

from .views import GoogleLogin, GoogleLoginCallback

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('/signup/', include('dj_rest_auth.registration.urls')),
    path('signup/google/', GoogleLogin.as_view(), name='google_login'),
]
