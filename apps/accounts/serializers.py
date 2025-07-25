from rest_framework import serializers
from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetSmsCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class ReturnGetSmsCodeSerializer(serializers.Serializer):
    sms_code = serializers.CharField()
    lifetime_sms_code = serializers.CharField()


class AuthenticateSmsCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    sms_code = serializers.CharField(required=True)

    def validate_sms_code(self, value):
        if len(value) != 4:
            raise ValidationError('Code is not valid')
        return value


class ListUsersSerializser(serializers.Serializer):
    phone_number = serializers.CharField()


class InviteUsersSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

    def validate_invite_code(self, value):
        if len(value) != 6:
            raise ValidationError('Code is not valid')
        return value