# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from cooperatives.models import Membership, Cooperative
from meters.models import Meter  # Додано для роботи з лічильниками
from .forms import CustomUserCreationForm


def home(request):
    """Головна сторінка сайту"""
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """Особистий кабінет користувача"""
    # 1. Перевіряємо, чи є користувач головою кооперативу
    # Якщо так — перенаправляємо в адмін-панель управління (staff)
    membership = Membership.objects.filter(user=request.user).first()
    if membership and membership.role == 'chairman':
        return redirect('staff_dashboard')

    # 2. Перевіряємо, чи підтверджено анкету мешканця головою
    if not request.user.is_approved:
        coop = Cooperative.objects.filter(id=request.user.coop_id).first()
        coop_name = coop.title if coop else "кооперативу"
        return render(
            request, 'registration/pending_approval.html',
            {'coop_name': coop_name})

    # 3. Логіка для підтвердженого мешканця
    # Знаходимо лічильник, прив'язаний до членства користувача
    meter = Meter.objects.filter(membership=membership).first()

    # Отримуємо історію останніх 5 показників для відображення в кабінеті
    readings = []
    if meter:
        # Використовуємо related_name='readings' з вашої моделі Reading
        readings = meter.readings.all()[:5]

    # Передаємо лічильник та історію в шаблон users/dashboard.html
    return render(
        request, 'users/dashboard.html', {
            'meter': meter,
            'readings': readings
            })


def register(request):
    """Реєстрація нового мешканця"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Нові користувачі завжди потребують підтвердження головою
            user.is_approved = False
            user.save()

            # Знаходимо назву кооперативу для сторінки очікування
            coop = Cooperative.objects.filter(id=user.coop_id).first()
            coop_name = coop.title if coop else "кооперативу"

            # Виходимо із системи, щоб мешканець не зайшов у кабінет до схвалення
            auth_logout(request)
            return render(
                request, 'registration/pending_approval.html',
                {'coop_name': coop_name})
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})