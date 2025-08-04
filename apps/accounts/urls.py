"""accounts url"""
from django.urls import path, include

urlpatterns = [
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/signup/', include('dj_rest_auth.registration.urls'))
]
