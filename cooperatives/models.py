from django.db import models
from django.conf import settings


class Cooperative(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва кооперативу")
    inn = models.CharField(max_length=20, verbose_name="ЄДРПОУ", blank=True)

    class Meta:
        verbose_name = "Кооператив"
        verbose_name_plural = "Кооперативи"

    def __str__(self):
        return self.title


class Membership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Учасник'),
        ('chairman', 'Голова правління'),
        ('vice_chairman','Зам голови'),
        ('accountant', 'Бухгалтер'),
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Користувач"
        )

    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        verbose_name="Кооператив"
        )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name="Роль"
        )

    plot_number = models.CharField(
        max_length=20, verbose_name="Номер ділянки/квартири")
    date_joined = models.DateField(
        auto_now_add=True, verbose_name="Дата вступу")

    class Meta:
        verbose_name = "Член кооперативу"
        verbose_name_plural = "Члени кооперативів"

    def __str__(self):
        return f"{self.user} - {self.cooperative} ({self.get_role_display()})"