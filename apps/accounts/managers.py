from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number

from apps.accounts.utils import generate_invite_code


class CustomUserManager(BaseUserManager):
    def validate_phone_number(self, phone_number: str) -> str:
        'Validate the phone number format and return a standardized version.'
        if not phone_number.startswith('+'):
            phone_number += '+'
        obj_phone = parse(phone_number)
        check_obj_phone = is_valid_number(obj_phone)
        if not check_obj_phone:
            raise ValidationError('Incorrect number entered')
        return f'+{obj_phone.country_code}{obj_phone.national_number}'

    def get_or_create_user(self, phone_number: str):
        'Get or create a user'
        phone_number = self.validate_phone_number(phone_number)
        user, created = self.model.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                'invite_code': generate_invite_code(),
            }
        )
        return user