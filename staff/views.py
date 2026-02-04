import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import chairman_required, staff_required
from users.models import CustomUser
from cooperatives.models import Membership, Cooperative, Street
from meters.models import Meter, Reading
from .forms import *
from datetime import timedelta


@login_required
@staff_required
def staff_dashboard(request):
    """Головна панель: Голова бачить все, Бухгалтер — лише навігацію"""
    membership = Membership.objects.get(
        user=request.user, role__in=['chairman', 'accountant'])
    cooperative = membership.cooperative

    streets = Street.objects.filter(cooperative=cooperative)

    form = StreetForm()

    residents = []
    if membership.role == 'chairman':
        residents = CustomUser.objects.filter(
            coop_id=cooperative.id, is_approved=False)

    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            new_street = form.save(commit=False)
            new_street.cooperative = cooperative
            new_street.save()
            messages.success(request, f"Вулицю {new_street.name} додано.")
            return redirect('staff_dashboard')

    return render(
        request, 'staff/dashboard.html', {
            'cooperative': cooperative,
            'residents': residents,
            'user_role': membership.role,
            'streets': streets,
            'form': form,
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
@staff_required
def edit_member(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=membership.user)
        m_form = MembershipUpdateForm(request.POST, instance=membership)

        if u_form.is_valid() and m_form.is_valid():
            u_form.save()
            m_form.save()
            messages.success(
                request,
                f"Дані користувача {membership.user.username} оновлено!")
            return redirect(
                'staff_manage')
    else:
        u_form = UserUpdateForm(instance=membership.user)
        m_form = MembershipUpdateForm(instance=membership)

    return render(
        request, 'staff/edit_member.html', {
            'u_form': u_form,
            'm_form': m_form,
            'membership': membership
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
@staff_required
@login_required
@staff_required
def manage_streets(request):
    """Додавання нової вулиці (POST) та перегляд (GET)"""
    membership = Membership.objects.filter(user=request.user).first()
    coop = membership.cooperative if membership else None
    streets = Street.objects.filter(
        cooperative=coop) if coop else Street.objects.none()

    if request.method == 'POST':
        form = StreetForm(request.POST)
        if form.is_valid():
            street = form.save(commit=False)
            street.cooperative = coop
            street.save()
            messages.success(request, f"Вулицю {street.name} успішно додано.")
            return redirect('staff_dashboard')
    else:
        form = StreetForm()

    return render(
        request, 'staff/cards/streets.html', {
            'streets': streets,
            'form': form
            })


@login_required
@staff_required
def edit_street(request, street_id):
    """Редагування назви існуючої вулиці"""
    street = get_object_or_404(Street, id=street_id)

    if request.method == 'POST':
        form = StreetForm(request.POST, instance=street)
        if form.is_valid():
            form.save()
            messages.success(request, f"Назву вулиці змінено на {street.name}.")
            return redirect('staff_dashboard')
    else:
        form = StreetForm(instance=street)

    return render(
        request, 'staff/edit_street.html', {
            'form': form,
            'street': street
            })


@login_required
@staff_required
def delete_street(request, street_id):
    """Видалення вулиці"""
    street = get_object_or_404(Street, id=street_id)

    if request.method == 'POST':
        name = street.name
        street.delete()
        messages.warning(request, f"Вулицю {name} видалено.")

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
@staff_required
def add_reading(request, membership_id):
    target_membership = get_object_or_404(Membership, id=membership_id)
    meter = Meter.objects.filter(membership=target_membership).first()

    if not meter:
        messages.error(
            request,
            f"У мешканця {target_membership.user.username} немає лічильника.")
        return redirect('staff_dashboard')

    today = timezone.localdate()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]

    is_submission_window_open = (today.day == last_day_of_month) or (
            today.day == 1)

    if not is_submission_window_open:
        messages.warning(
            request,
            f"Подача показників закрита! Дозволено лише в останній день місяця або 1-го числа.")

    reporting_date = today - timedelta(days=1) if today.day == 1 else today

    has_reading_this_month = Reading.objects.filter(
        meter=meter,
        date__year=reporting_date.year,
        date__month=reporting_date.month
        ).exists()

    previous = Reading.objects.filter(meter=meter).order_by(
        '-date', '-id').first()

    if request.method == 'POST':
        if not is_submission_window_open:
            messages.error(
                request, "Помилка! Подача показників зараз заборонена.")
            return redirect('staff_readings')

        if has_reading_this_month:
            messages.error(
                request,
                f"Помилка! Показники за {reporting_date.strftime('%B')} вже подано.")
            return redirect('staff_readings')

        try:
            v_day = float(
                request.POST.get('value_day', 0)) if meter.is_two_zone else 0
            v_night = float(
                request.POST.get('value_night', 0)) if meter.is_two_zone else 0
            v_total = float(
                request.POST.get(
                    'value_total', 0)) if not meter.is_two_zone else (
                    v_day + v_night)

            if previous:
                pass

            Reading.objects.create(
                meter=meter,
                value_day=v_day if meter.is_two_zone else None,
                value_night=v_night if meter.is_two_zone else None,
                value_total=v_total,
                submitted_by=request.user,
                )
            messages.success(request, "Показники успішно додано.")
            return redirect('staff_readings')

        except ValueError:
            messages.error(request, "Введіть коректні числа.")

    return render(
        request, 'staff/add_reading.html', {
            'target_member': target_membership,
            'meter': meter,
            'previous': previous,
            'is_window_open': is_submission_window_open,
            'has_reading': has_reading_this_month
            })


@login_required
@staff_required
def find_meter_by_number(request):
    """Сторінка вводу номеру лічильника для переходу до додавання показників"""
    if request.method == 'POST':
        meter_number = request.POST.get('meter_number')

        try:
            meter = Meter.objects.get(number=meter_number)

            if meter.membership:
                return redirect(
                    'add_reading', membership_id=meter.membership.id)
            else:
                messages.error(
                    request,
                    f"Лічильник №{meter_number} знайдено, але він не прив'язаний до жодного мешканця!")

        except Meter.DoesNotExist:
            messages.error(
                request, f"Лічильник з номером '{meter_number}' не знайдено.")

    return render(request, 'staff/find_meter.html')
