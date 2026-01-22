from django.db import models
from django.conf import settings


class Cooperative(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва кооперативу")
    inn = models.CharField(max_length=20, verbose_name="ЄДРПОУ", blank=True)
    price_day = models.DecimalField(
        max_digits=10, decimal_places=2, default=2.64,
        verbose_name="Тариф День (грн/кВт)")
    price_night = models.DecimalField(
        max_digits=10, decimal_places=2, default=1.32,
        verbose_name="Тариф Ніч (грн/кВт)")
    class Meta:
        verbose_name = "Кооператив"
        verbose_name_plural = "Кооперативи"

    def __str__(self):
        return self.title


class Street(models.Model):
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
        address = f"{self.street.name}, {self.plot_number}" if self.street else f"Діл. {self.plot_number}"
        return f"{address} ({self.user.username})"



class CooperativeApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова заявка'),
        ('approved', 'Схвалено'),
        ('rejected', 'Відхилено'),
    ]

    name = models.CharField("Назва кооперативу", max_length=200)
    address = models.CharField("Адреса будинку", max_length=255)
    contact_name = models.CharField("ПІБ Голови/Контактної особи", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email для зв'язку")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Заявка від {self.name} ({self.contact_name})"

    class Meta:
        verbose_name = "Заявка на кооператив"
        verbose_name_plural = "Заявки на кооперативи"
