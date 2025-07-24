from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.views import api_views, app_views


urlpatterns = [
    path(
        'api/token/',
        api_views.AuthenticateSmsCodeAPIView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/sms-code/',
        api_views.GetSmsCodeAPIView.as_view(),
        name='get-sms-code'
    ),
    path('api/list-users/', api_views.ListUsers.as_view(), name='list-users')
]