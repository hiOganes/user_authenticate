from django.urls import path

from apps.accounts import views

urlpatterns = [
    path(
        'api/token/',
        views.AuthenticateSmsCodeAPIView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        views.CustomTokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/sms-code/',
        views.GetSmsCodeAPIView.as_view(),
        name='get-sms-code'
    ),
    path('api/list-users/', views.ListUsers.as_view(), name='list-users'),
    path(
        'api/invite-code/',
        views.ActivateInviteCode.as_view(),
        name='invite-code'
    ),
    path(
        'api/check/invite-code/',
        views.CheckInviteCodeAPIView.as_view(),
        name='check-invite-code'
    )
]