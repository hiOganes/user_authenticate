from rest_framework import status
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer
)
from drf_spectacular.utils import (
    OpenApiParameter, OpenApiExample, OpenApiRequest
)

from apps.accounts import serializers

# tags

TAGS_AUTH = ['Auth']
TAGS_ACCOUNTS = ['Account']

# description
POST_GET_SMS_CODE_APIVIEW_DESCRIPTION = '''
    Accepts phone number and sends SMS code. 
    If the user enters the first time, writes it to the database. 
    Returns the code that must be sent via SMS and his lifetime.
    '''

POST_AUTHENTICATE_SMS_CODE_APIVIEW_DESCRIPTION = '''
    Accepts code from SMS and returns "access" and "refresh" tokens.
    '''

CUSTOM_TOKEN_REFRESH_VIEW_DESCRIPTION = '''
    Replaces previously issued tokens.
    '''

POST_ACTIVATE_INVITE_CODE_DESCRIPTION = '''
    Allows the user to activate his invitation code and is returned.
    '''

POST_CHECK_INVITE_CODE_APIVIEW_DESCRIPTION = '''
    Allows you to check if this invitation code exists.
    '''

GET_LIST_USERS_DESCRIPTION = '''
Rturn all user numbers who used this users invitation code.
'''


# responses
POST_GET_SMS_CODE_APIVIEW_RESPONSES = {
    status.HTTP_200_OK: serializers.ReturnGetSmsCodeSerializer,
    status.HTTP_400_BAD_REQUEST: serializers.ReturnGetSmsCodeSerializer
}

POST_AUTHENTICATE_SMS_CODE_APIVIEW_RESPONSES = {
    status.HTTP_200_OK: TokenObtainPairSerializer,
    status.HTTP_400_BAD_REQUEST: TokenObtainPairSerializer,
}

# CUSTOM_TOKEN_REFRESH_VIEW_RESPONSES = {}

POST_ACTIVATE_INVITE_CODE_RESPONSES = {
    status.HTTP_201_CREATED: serializers.InviteUsersSerializer,
    status.HTTP_400_BAD_REQUEST: serializers.InviteUsersSerializer,
}

POST_CHECK_INVITE_CODE_APIVIEW_RESPONSES = {
    status.HTTP_200_OK: serializers.InviteUsersSerializer,
    status.HTTP_404_NOT_FOUND: serializers.InviteUsersSerializer,
}

GET_LIST_USERS_RESPONSES = {
    status.HTTP_200_OK: serializers.ListUsersSerializser,
}