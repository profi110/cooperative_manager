from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Meter, Reading
from cooperatives.models import Membership

@login_required
def submit_reading(request):
    """Подача показників мешканцем з перевіркою наявності лічильника"""
    membership = Membership.objects.filter(user=request.user).first()

    meter = Meter.objects.filter(membership=membership).first()

    if not meter:
        messages.error(
            request,
            "За вами ще не закріплено жодного лічильника. Зверніться до голови.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        val_total = request.POST.get('value_total')
        val_day = request.POST.get('value_day')
        val_night = request.POST.get('value_night')
        photo = request.FILES.get('photo')

        Reading.objects.create(
            meter=meter,
            value_total=val_total if val_total else 0,
            value_day=val_day,
            value_night=val_night,
            photo=photo,
            submitted_by=request.user
            )
        messages.success(request, "Показники успішно подано!")
        return redirect('user_dashboard')

    return render(request, 'meters/submit_reading.html', {'meter': meter})
