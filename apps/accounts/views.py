from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from apps.accounts.models import User
from apps.accounts.utils import create_sms_code, send_sms
from apps.accounts import schema_examples
from apps.accounts.serializers import (
    GetSmsCodeSerializer, AuthenticateSmsCodeSerializer, ListUsersSerializser,
    InviteUsersSerializer
)


class GetSmsCodeAPIView(APIView):
    serializer_class = GetSmsCodeSerializer
    model = User

    @extend_schema(
        summary='This endpoint send and returns sms code.',
        description=schema_examples.POST_GET_SMS_CODE_APIVIEW_DESCRIPTION,
        responses=schema_examples.POST_GET_SMS_CODE_APIVIEW_RESPONSES,
        tags=schema_examples.TAGS_AUTH
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.model.objects.get_or_create_user(
                serializer.validated_data['phone_number']
            )
            user.sms_code = create_sms_code()
            user.lifetime_sms_code = timezone.now() + timedelta(minutes=5)
            user.save()
            send_sms(user.phone_number, user.sms_code)
            return Response(
                data={
                    'sms_code': user.sms_code,
                    'lifetime_sms_code': user.lifetime_sms_code
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.error, status=status.HTTP_400_BAD_REQUEST
        )


class AuthenticateSmsCodeAPIView(APIView):
    serializer_class = AuthenticateSmsCodeSerializer
    model_class = User

    @extend_schema(
        summary='This endpoin return access and refresh tokens',
        description=schema_examples.POST_AUTHENTICATE_SMS_CODE_APIVIEW_DESCRIPTION,
        responses=schema_examples.POST_AUTHENTICATE_SMS_CODE_APIVIEW_RESPONSES,
        tags=schema_examples.TAGS_AUTH
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            sms_code = serializer.validated_data['sms_code']
            user = self.model_class.objects.get(
                phone_number=phone_number
            )
            if user.lifetime_sms_code < timezone.now():
                return Response(
                    data={'message': 'The code has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            if user.is_staff:
                refresh.payload.update({'group': 'admin'})
            else:
                refresh.payload.update({'group': 'user'})
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        summary='This endpoin return new access and refresh tokens',
        description=schema_examples.CUSTOM_TOKEN_REFRESH_VIEW_DESCRIPTION,
        tags=schema_examples.TAGS_AUTH
    )
class CustomTokenRefreshView(TokenRefreshView):
    pass


class ActivateInviteCode(APIView):
    serializer_class = InviteUsersSerializer
    model_class = User
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='This endpoint activate invite code',
        description=schema_examples.POST_ACTIVATE_INVITE_CODE_DESCRIPTION,
        responses=schema_examples.POST_ACTIVATE_INVITE_CODE_RESPONSES,
        tags=schema_examples.TAGS_ACCOUNTS
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            from_user = request.user
            to_user = self.model_class.objects.filter(
                invite_code=invite_code
            ).first()
            if request.user.invite_status_code:
                return Response(
                    data={'message': 'Активировать можно 1 раз'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not to_user:
                return Response(
                    data={'message': 'Пользователь не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            from_user.invite_users.add(to_user)
            from_user.invite_status_code = True
            from_user.save(update_fields=['invite_status_code'])
            serializer = self.serializer_class(to_user)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CheckInviteCodeAPIView(APIView):
    serializer_class = InviteUsersSerializer
    model_class = User
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='This endpoint check invite code',
        description=schema_examples.POST_CHECK_INVITE_CODE_APIVIEW_DESCRIPTION,
        responses=schema_examples.POST_CHECK_INVITE_CODE_APIVIEW_RESPONSES,
        tags=schema_examples.TAGS_ACCOUNTS
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            invite_code = self.model_class.objects.filter(
                invite_code=serializer.validated_data['invite_code']
            ).first()
            if invite_code:
                return Response(
                    data={'message': 'invite code is vslid'},
                    status=status.HTTP_200_OK
                )
            return Response(
                data={'massage': 'invite code is not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ListUsers(APIView):
    serializer_class = ListUsersSerializser
    model_class = User
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='This endpoint return list invite users',
        description=schema_examples.GET_LIST_USERS_DESCRIPTION,
        responses=schema_examples.GET_LIST_USERS_RESPONSES,
        tags=schema_examples.TAGS_ACCOUNTS
    )
    def get(self, request, *args, **kwargs):
        invite_users = request.user.invite_by.all()
        serializer = self.serializer_class(invite_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)