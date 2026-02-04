import calendar
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Meter, Reading
from cooperatives.models import Membership


@login_required
def submit_reading(request):
    """Подача показників мешканцем з обмеженням по даті"""
    membership = Membership.objects.filter(user=request.user).first()
    meter = Meter.objects.filter(membership=membership).first()

    if not meter:
        messages.error(
            request,
            "За вами ще не закріплено жодного лічильника. Зверніться до голови.")
        return redirect('user_dashboard')

    today = timezone.localdate()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]

    is_window_open = (today.day == 1) or (today.day == last_day_of_month)

    reporting_date = today - timedelta(days=1) if today.day == 1 else today

    has_reading = Reading.objects.filter(
        meter=meter,
        date__year=reporting_date.year,
        date__month=reporting_date.month
        ).exists()

    if request.method == 'POST':
        if not is_window_open:
            messages.error(request, "Подача показників зараз закрита.")
            return redirect('submit_reading')

        if has_reading:
            messages.warning(request, "Ви вже подали показники за цей місяць.")
            return redirect('submit_reading')

        try:
            val_total = request.POST.get('value_total')
            val_day = request.POST.get('value_day')
            val_night = request.POST.get('value_night')
            photo = request.FILES.get('photo')

            if meter.is_two_zone and val_day and val_night:
                calculated_total = float(val_day) + float(val_night)
            else:
                calculated_total = float(val_total) if val_total else 0

            Reading.objects.create(
                meter=meter,
                value_total=calculated_total,
                value_day=float(val_day) if val_day else None,
                value_night=float(val_night) if val_night else None,
                photo=photo,
                submitted_by=request.user
                )
            messages.success(request, "Показники успішно подано!")
            return redirect('user_dashboard')

        except ValueError:
            messages.error(request, "Будь ласка, введіть коректні числа.")

    return render(
        request, 'meters/submit_reading.html', {
            'meter': meter,
            'is_window_open': is_window_open,
            'has_reading': has_reading
            })
