from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse

# Імпортуємо моделі та форми один раз
from cooperatives.models import Membership, Cooperative
from meters.models import Meter
from .models import CustomUser
from .forms import CustomUserCreationForm

# --- API Ендпоінти ---

def check_coop_id_api(request):
    """API для перевірки існування кооперативу та отримання вулиць через fetch"""
    coop_id = request.GET.get('coop_id', None)
    data = {
        'exists': False,
        'name': '',
        'streets': []
    }

    if coop_id:
        try:
            cooperative = Cooperative.objects.get(id=coop_id)
            data['exists'] = True
            # Використовуємо title або name залежно від твоєї моделі
            data['name'] = getattr(cooperative, 'title', getattr(cooperative, 'name', ''))
            data['streets'] = list(cooperative.street_set.values_list('name', flat=True))
        except (Cooperative.DoesNotExist, ValueError):
            pass

    return JsonResponse(data)

def check_duplicates_api(request):
    """API для перевірки унікальності логіна або телефону"""
    username = request.GET.get('username', None)
    phone = request.GET.get('phone', None)
    data = {'is_taken': False}

    if username:
        data['is_taken'] = CustomUser.objects.filter(username__iexact=username).exists()

    if phone:
        data['is_taken'] = CustomUser.objects.filter(phone_number=phone).exists()

    return JsonResponse(data)

# --- Сторінки користувача ---

def home(request):
    """Головна сторінка сайту"""
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """Особистий кабінет з редіректом за роллю та перевіркою схвалення"""
    membership = Membership.objects.filter(user=request.user).first()

    # Якщо користувач — голова або бухгалтер, відправляємо в адмін-панель
    if membership and membership.role in ['chairman', 'accountant']:
        return redirect('staff_dashboard')

    # Якщо реєстрація ще не схвалена головою
    if not request.user.is_approved:
        coop = Cooperative.objects.filter(id=request.user.coop_id).first()
        coop_name = coop.title if coop else "кооперативу"
        return render(request, 'registration/pending_approval.html', {'coop_name': coop_name})

    # Відображення показників для звичайного мешканця
    meter = Meter.objects.filter(membership=membership).first()
    readings = meter.readings.all()[:5] if meter else []

    return render(request, 'users/dashboard.html', {
        'meter': meter,
        'readings': readings,
        'membership': membership
    })

def register(request):
    """Реєстрація нового мешканця з автоматичним статусом очікування"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Користувач чекає на схвалення
            user.save()

            coop = Cooperative.objects.filter(id=user.coop_id).first()
            coop_name = coop.title if coop else "кооперативу"

            # Розлогінюємо користувача, щоб він не міг зайти до схвалення
            auth_logout(request)
            return render(request, 'registration/pending_approval.html', {'coop_name': coop_name})
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})