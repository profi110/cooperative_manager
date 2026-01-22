# meters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Meter, Reading
from .forms import ReadingForm
from cooperatives.models import Membership

@login_required
def submit_reading(request):
    # 1. Знаходимо членство та лічильник мешканця
    membership = Membership.objects.filter(user=request.user, role='resident').first()
    meter = get_object_or_404(Meter, membership=membership)

    if request.method == 'POST':
        # Передаємо FILES для завантаження фото
        form = ReadingForm(request.POST, request.FILES, is_two_zone=meter.is_two_zone)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.meter = meter
            reading.submitted_by = request.user
            reading.save()
            return redirect('user_dashboard') # Повертаємо в кабінет
    else:
        form = ReadingForm(is_two_zone=meter.is_two_zone)

    return render(request, 'meters/submit_reading.html', {
        'form': form,
        'meter': meter
    })