from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        unique=True
    )
    sms_code = models.CharField(
        max_length=6,
        verbose_name = 'Код из СМС',
        blank=True,
        null=True
    )
    invite_code = models.CharField(
        max_length=6,
        verbose_name='Код приглашения',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'