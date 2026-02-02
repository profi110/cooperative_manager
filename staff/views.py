import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import chairman_required, staff_required
from users.models import CustomUser
from cooperatives.models import Membership, Cooperative, Street
from meters.models import Meter, Reading



@login_required
@staff_required
def staff_dashboard(request):
    """Головна панель: Голова бачить все, Бухгалтер — лише навігацію"""
    membership = Membership.objects.get(
        user=request.user, role__in=['chairman', 'accountant'])
    cooperative = membership.cooperative

    residents = []
    if membership.role == 'chairman':
        residents = CustomUser.objects.filter(
            coop_id=cooperative.id, is_approved=False)

    return render(
        request, 'staff/dashboard.html', {
            'cooperative': cooperative,
            'residents': residents,
            'user_role': membership.role
            })



@login_required
@staff_required
def all_readings(request):
    """Список всіх показників для персоналу"""
    membership = Membership.objects.get(
        user=request.user, role__in=['chairman', 'accountant'])
    readings = Reading.objects.filter(
        meter__cooperative=membership.cooperative
        ).order_by('-date')

    return render(
        request, 'staff/all_readings.html', {
            'readings': readings,
            'cooperative': membership.cooperative,
            'user_role': membership.role
            })


@login_required
@staff_required
def edit_reading(request, reading_id):
    """Редагування показників з перевіркою на зменшення значень"""
    reading = get_object_or_404(Reading, id=reading_id)
    membership = Membership.objects.get(
        user=request.user, role__in=['chairman', 'accountant'])

    previous = Reading.objects.filter(
        meter=reading.meter,
        date__lt=reading.date
        ).order_by('-date').first()

    if request.method == 'POST':
        try:
            if reading.meter.is_two_zone:
                val_day = float(request.POST.get('value_day', 0))
                val_night = float(request.POST.get('value_night', 0))

                if previous:
                    if val_day < float(
                            previous.value_day or 0) or val_night < float(
                            previous.value_night or 0):
                        messages.error(
                            request,
                            "Показники не можуть бути меншими за попередні!")
                        return render(
                            request, 'staff/edit_reading.html', {
                                'reading': reading, 'user_role': membership.role
                                })

                reading.value_day = val_day
                reading.value_night = val_night
                reading.value_total = val_day + val_night
            else:
                val_total = float(request.POST.get('value_total', 0))
                if previous and val_total < float(previous.value_total):
                    messages.error(
                        request, "Показник не може бути меншим за попередній!")
                    return render(
                        request, 'staff/edit_reading.html', {
                            'reading': reading, 'user_role': membership.role
                            })

                reading.value_total = val_total

            reading.save()
            messages.success(request, "Показники успішно оновлено.")
            return redirect('staff_readings')
        except ValueError:
            messages.error(request, "Будь ласка, введіть числові значення.")

    return render(
        request, 'staff/edit_reading.html',
        {'reading': reading, 'user_role': membership.role})



@login_required
@chairman_required
def approve_resident(request, user_id):
    """Схвалення мешканця та створення лічильника (Вулиця + Ділянка)"""
    if request.method == 'POST':
        resident = get_object_or_404(CustomUser, id=user_id)
        plot_val = request.POST.get('plot_number')
        meter_type = request.POST.get('meter_type')
        resident.is_approved = True
        resident.save()

        ch_mem = Membership.objects.get(user=request.user, role='chairman')
        street_obj = Street.objects.filter(
            name=resident.street, cooperative=ch_mem.cooperative).first()

        res_mem, _ = Membership.objects.get_or_create(
            user=resident, cooperative=ch_mem.cooperative,
            defaults={
                'role': 'member', 'street': street_obj, 'plot_number': plot_val
                }
            )

        street_digits = "".join(
            re.findall(r'\d+', street_obj.name)) if street_obj else "0"
        serial = f"{street_digits}{plot_val}"

        Meter.objects.get_or_create(
            number=serial, cooperative=ch_mem.cooperative,
            defaults={
                'membership': res_mem, 'street': street_obj,
                'is_two_zone': (meter_type == 'two_zone')
                }
            )
        messages.success(
            request, f"Мешканця схвалено. Створено лічильник №{serial}")
    return redirect('staff_dashboard')


@login_required
@chairman_required
def manage_coop(request):
    """Список всіх мешканців кооперативу"""
    ch_mem = Membership.objects.get(user=request.user, role='chairman')
    members = Membership.objects.filter(
        cooperative=ch_mem.cooperative
        ).exclude(user=request.user).select_related('user', 'street')

    return render(
        request, 'staff/manage.html', {
            'members': members,
            'cooperative': ch_mem.cooperative,
            'user_role': ch_mem.role
            })


@login_required
@chairman_required
def edit_member(request, membership_id):
    """Редагування даних мешканця або зміна ролі (наприклад, на Бухгалтера)"""
    membership = get_object_or_404(Membership, id=membership_id)
    ch_mem = Membership.objects.get(user=request.user, role='chairman')

    if request.method == 'POST':
        user = membership.user
        user.username = request.POST.get('username')
        user.save()

        membership.plot_number = request.POST.get('plot_number')
        membership.role = request.POST.get(
            'role')

        street_id = request.POST.get('street')
        if street_id:
            membership.street = Street.objects.get(id=street_id)

        membership.save()
        messages.success(request, "Дані мешканця оновлено.")
        return redirect('staff_manage')

    streets = Street.objects.filter(cooperative=ch_mem.cooperative)
    return render(
        request, 'staff/edit_member.html', {
            'membership': membership,
            'streets': streets,
            'user_role': ch_mem.role
            })


@login_required
@chairman_required
def delete_member(request, membership_id):
    if request.method == 'POST':
        membership = get_object_or_404(Membership, id=membership_id)
        if membership.cooperative == Membership.objects.get(
                user=request.user, role='chairman').cooperative:
            membership.user.delete()
            messages.success(request, "Мешканця видалено.")
    return redirect('staff_manage')



@login_required
@chairman_required
def update_tariffs(request):
    if request.method == 'POST':
        coop = Membership.objects.get(
            user=request.user, role='chairman').cooperative
        coop.price_day = request.POST.get('price_day')
        coop.price_night = request.POST.get('price_night')
        coop.save()
        messages.success(request, "Тарифи оновлено.")
    return redirect('staff_dashboard')


@login_required
@chairman_required
def add_street(request):
    if request.method == 'POST':
        name = request.POST.get('street_name')
        coop = Membership.objects.get(
            user=request.user, role='chairman').cooperative
        if name:
            Street.objects.create(cooperative=coop, name=name)
            messages.success(request, f"Вулицю {name} додано.")
    return redirect('staff_dashboard')


@login_required
@chairman_required
def edit_street(request, street_id):
    street = get_object_or_404(Street, id=street_id)
    if request.method == 'POST':
        street.name = request.POST.get('street_name')
        street.save()
        return redirect('staff_dashboard')
    return render(
        request, 'staff/edit_street.html',
        {'street': street, 'user_role': 'chairman'})


@login_required
@chairman_required
def delete_street(request, street_id):
    if request.method == 'POST':
        Street.objects.get(id=street_id).delete()
    return redirect('staff_dashboard')



@login_required
@staff_required
def voting_list(request):
    """Доступно і Голові, і Бухгалтеру"""
    membership = Membership.objects.get(
        user=request.user, role__in=['chairman', 'accountant'])
    return render(
        request, 'staff/voting.html', {
            'user_role': membership.role,
            'cooperative': membership.cooperative
            })
