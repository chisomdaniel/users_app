"""accounts url"""
from django.urls import path, include

from .views import GoogleLogin, GoogleLoginCallback, VerifyEmailCodeView, ProfileImage

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('signup/google/', GoogleLogin.as_view(), name='google_login'),
    path('verify-email-code/', VerifyEmailCodeView.as_view(), name='verify-email-code'),
    path('upload-image/', ProfileImage.as_view(), name='upload-user-image'),
]
