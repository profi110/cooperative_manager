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


class Street(models.Model):
    """
    Ми перенесли Вулицю сюди, бо вона є частиною Кооперативу,
    а не просто властивістю лічильника.
    """
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        verbose_name="Кооператив"
        )
    name = models.CharField(max_length=100, verbose_name="Назва вулиці")

    class Meta:
        verbose_name = "Вулиця"
        verbose_name_plural = "Вулиці"

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Учасник'),
        ('chairman', 'Голова правління'),
        ('vice_chairman', 'Зам голови'),
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

    # НОВЕ ПОЛЕ: Тепер людина прив'язана до вулиці
    street = models.ForeignKey(
        Street,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Вулиця"
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
        # Тепер у нас гарна адреса: "Вул. Садова, буд. 5 - Іван"
        address = f"{self.street.name}, {self.plot_number}" if self.street else f"Діл. {self.plot_number}"
        return f"{address} ({self.user.username})"