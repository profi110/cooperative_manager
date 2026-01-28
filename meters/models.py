from django.db import models
from django.conf import settings
from cooperatives.models import Cooperative, Membership, Street


class Meter(models.Model):
    """Модель лічильника для обліку електроенергії в кооперативі"""
    TYPE_CHOICES = [('el', 'Електроенергія')]
    HIERARCHY_CHOICES = [
        ('individual', 'Особистий (Будинок/Квартира)'),
        ('street', 'Вуличний (Баланс вулиці)'),
        ('global', 'Головний (Баланс кооперативу)'),
        ]

    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        verbose_name="Кооператив",
        null=True, blank=True)

    membership = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Власник")

    street = models.ForeignKey(
        Street,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вулиця")

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='el',
        verbose_name="Тип")

    hierarchy = models.CharField(
        max_length=20,
        choices=HIERARCHY_CHOICES,
        default='individual',
        verbose_name="Рівень")

    number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Серійний номер")

    is_two_zone = models.BooleanField(
        default=False,
        verbose_name="Двозонний (День/Ніч)")

    initial_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Початковий показник")

    class Meta:
        verbose_name = "Лічильник"
        verbose_name_plural = "Лічильники"

    def __str__(self):
        return f"№{self.number} ({'День/Ніч' if self.is_two_zone else 'Звичайний'})"


class Reading(models.Model):
    """Модель показників лічильника з автоматичним розрахунком вартості"""
    meter = models.ForeignKey(
        Meter,
        on_delete=models.CASCADE,
        verbose_name="Лічильник",
        related_name='readings')

    value_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Загальний (Т)")

    value_day = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="День (Т1)")

    value_night = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Ніч (Т2)")

    # ВИПРАВЛЕНО: DateTimeField замість DateField для підтримки формату H:i
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата подачі")

    photo = models.ImageField(
        upload_to='readings/',
        blank=True,
        null=True,
        verbose_name="Фото")

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Ким подано")

    class Meta:
        verbose_name = "Показник"
        verbose_name_plural = "Показники (Історія)"
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """Автоматичне підсумовування показників перед збереженням"""
        if self.meter.is_two_zone and self.value_day is not None and self.value_night is not None:
            self.value_total = self.value_day + self.value_night
        super().save(*args, **kwargs)

    def get_cost(self):
        """Розрахунок вартості на основі тарифів кооперативу"""
        previous = Reading.objects.filter(
            meter=self.meter,
            date__lt=self.date
            ).order_by('-date').first()

        p_total = previous.value_total if previous else self.meter.initial_value
        p_day = previous.value_day if (previous and previous.value_day) else 0
        p_night = previous.value_night if (
                    previous and previous.value_night) else 0

        coop = self.meter.cooperative

        # Формула розрахунку вартості для двозонного обліку
        if self.meter.is_two_zone:
            diff_day = self.value_day - p_day
            diff_night = self.value_night - p_night
            return (diff_day * coop.price_day) + (diff_night * coop.price_night)

        # Стандартна формула
        return (self.value_total - p_total) * coop.price_day

    def __str__(self):
        return f"{self.meter.number}: {self.value_total}"