import re
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .forms import CustomUserCreationForm
from .models import CustomUser
from cooperatives.models import Cooperative
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from cooperatives.models import Membership



class DuplicateCheckThrottle(UserRateThrottle):
    rate = '10/hour'


@api_view(['GET'])
@throttle_classes([DuplicateCheckThrottle])
def api_check_duplicates(request):
    """API для перевірки унікальності логіна та телефону з вбудованим фільтром"""
    username = request.GET.get('username')
    phone = request.GET.get('phone')

    # Рівень 3: Регулярний вираз для валідації телефону перед зверненням до БД
    phone_pattern = re.compile(r'^\+?380\d{9}$|^0\d{9}$')

    if phone:
        # Перевірка формату: якщо це не номер, навіть не смикаємо базу
        if not phone_pattern.match(phone):
            return Response(
                {'is_taken': False, 'error': 'Invalid format'}, status=200)

        is_taken = CustomUser.objects.filter(phone_number=phone).exists()
        return Response({'is_taken': is_taken})

    if username:
        # Мінімальна перевірка довжини логіна
        if len(username) < 3:
            return Response({'is_taken': False})

        is_taken = CustomUser.objects.filter(username=username).exists()
        return Response({'is_taken': is_taken})

    return Response({'error': 'No data provided'}, status=400)

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


def home(request):
    """Головна сторінка сайту"""
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """Особистий кабінет з редіректом за роллю та перевіркою схвалення"""
    membership = Membership.objects.filter(user=request.user).first()

    if membership and membership.role in ['chairman', 'accountant']:
        return redirect('staff_dashboard')

    if not request.user.is_approved:
        coop = Cooperative.objects.filter(id=request.user.coop_id).first()
        coop_name = coop.title if coop else "кооперативу"
        return render(request, 'registration/pending_approval.html', {'coop_name': coop_name})

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
            user.is_approved = False
            user.save()

            coop = Cooperative.objects.filter(id=user.coop_id).first()
            coop_name = coop.title if coop else "кооперативу"

            auth_logout(request)
            return render(request, 'registration/pending_approval.html', {'coop_name': coop_name})
        else:
            print("Form errors:", form.errors.as_data())
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})