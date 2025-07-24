from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.accounts.managers import CustomUserManager


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
    lifetime_sms_code = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Срок действия смс кода'
    )
    invite_code = models.CharField(
        max_length=6,
        verbose_name='Код приглашения',
        blank=True,
        null=True
    )
    invite_users = models.ManyToManyField(
        'self',
        related_name='invite_users'
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

    objects = CustomUserManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'