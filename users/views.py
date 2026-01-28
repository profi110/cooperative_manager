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


# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from cooperatives.models import Membership, Cooperative
from meters.models import Meter
from .forms import CustomUserCreationForm


@login_required
def dashboard(request):
    """Особистий кабінет користувача з перенаправленням за роллю"""
    membership = Membership.objects.filter(user=request.user).first()

    # ЗМІНЕНО: додаємо перевірку на 'accountant'
    if membership and membership.role in ['chairman', 'accountant']:
        return redirect('staff_dashboard')

    if not request.user.is_approved:
        coop = Cooperative.objects.filter(id=request.user.coop_id).first()
        coop_name = coop.title if coop else "кооперативу"
        return render(
            request, 'registration/pending_approval.html',
            {'coop_name': coop_name})

    meter = Meter.objects.filter(membership=membership).first()
    readings = []
    if meter:
        readings = meter.readings.all()[:5]

    return render(
        request, 'users/dashboard.html', {
            'meter': meter,
            'readings': readings
            })


# ... решта функцій (home, register) залишаються без змін ...


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