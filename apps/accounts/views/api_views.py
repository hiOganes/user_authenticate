from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import (
    GetSmsCodeSerializer, AuthenticateSmsCodeSerializer, ListUsersSerializser
)
from apps.accounts.models import User
from apps.accounts.utils import create_sms_code, send_sms


class GetSmsCodeAPIView(APIView):
    serializer_class = GetSmsCodeSerializer
    model = User

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
                    'valid until': user.lifetime_sms_code
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.error, status=status.HTTP_400_BAD_REQUEST
        )


class AuthenticateSmsCodeAPIView(APIView):
    serializer_class = AuthenticateSmsCodeSerializer
    model_class = User

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


class ActivateInviteCode(APIView):
    serializer_class = ListUsersSerializser
    model_class = User
    permission_classes = [IsAuthenticated]


class ListUsers(APIView):
    serializer_class = ListUsersSerializser
    model_class = User
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        invite_users = request.user.invite_users.all()
        serializer = self.serializer_class(invite_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)