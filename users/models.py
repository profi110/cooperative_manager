from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон"
        )
    is_approved = models.BooleanField(default=False)
    coop_id = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=20, blank=True, null=True)
    house_number = models.CharField(
        max_length=10,
        verbose_name="Номер будинку",
        null=True,
        blank=True
        )
    def __str__(self):
        return self.username
