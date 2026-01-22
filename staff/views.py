# staff/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .decorators import chairman_required
from users.models import CustomUser
from cooperatives.models import Membership, Cooperative, Street
from meters.models import Meter, Reading  # Додано Reading


@login_required
@chairman_required
def staff_dashboard(request):
    membership = Membership.objects.get(user=request.user, role='chairman')
    cooperative = membership.cooperative
    residents = CustomUser.objects.filter(
        coop_id=cooperative.id, is_approved=False)
    return render(
        request, 'staff/dashboard.html',
        {'cooperative': cooperative, 'residents': residents})


@login_required
@chairman_required
def approve_resident(request, user_id):
    if request.method == 'POST':
        resident = get_object_or_404(CustomUser, id=user_id)
        plot_val = request.POST.get('plot_number')
        meter_type = request.POST.get('meter_type')
        resident.is_approved = True
        resident.save()

        chairman_mem = Membership.objects.get(
            user=request.user, role='chairman')
        coop = chairman_mem.cooperative
        street_obj = Street.objects.filter(
            name=resident.street, cooperative=coop).first()

        res_mem, _ = Membership.objects.get_or_create(
            user=resident, cooperative=coop,
            defaults={
                'role': 'member', 'street': street_obj, 'plot_number': plot_val
                }
            )

        serial = f"{street_obj.id if street_obj else '0'}{plot_val}"
        Meter.objects.get_or_create(
            number=serial, cooperative=coop,
            defaults={
                'membership': res_mem, 'street': street_obj,
                'is_two_zone': (meter_type == 'two_zone')
                }
            )
    return redirect('staff_dashboard')


@login_required
@chairman_required
def update_tariffs(request):
    if request.method == 'POST':
        membership = Membership.objects.get(user=request.user, role='chairman')
        coop = membership.cooperative
        coop.price_day = request.POST.get('price_day')
        coop.price_night = request.POST.get('price_night')
        coop.save()
    return redirect('staff_dashboard')


@login_required
@chairman_required
def all_readings(request):
    """НОВА ФУНКЦІЯ: Відображення історії всіх показників кооперативу"""
    membership = Membership.objects.get(user=request.user, role='chairman')
    cooperative = membership.cooperative
    # Отримуємо всі показники лічильників, що належать до цього кооперативу
    readings = Reading.objects.filter(meter__cooperative=cooperative).order_by(
        '-date')

    return render(
        request, 'staff/all_readings.html', {
            'readings': readings,
            'cooperative': cooperative
            })


# Функції для вулиць
@login_required
@chairman_required
def add_street(request):
    if request.method == 'POST':
        name = request.POST.get('street_name')
        membership = Membership.objects.get(user=request.user, role='chairman')
        if name:
            Street.objects.create(cooperative=membership.cooperative, name=name)
    return redirect('staff_dashboard')


@login_required
@chairman_required
def delete_street(request, street_id):
    membership = Membership.objects.get(user=request.user, role='chairman')
    street = get_object_or_404(
        Street, id=street_id, cooperative=membership.cooperative)
    if request.method == 'POST':
        street.delete()
    return redirect('staff_dashboard')