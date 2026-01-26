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


@login_required
@chairman_required
def add_street(request):
    """Додавання нової вулиці"""
    if request.method == 'POST':
        name = request.POST.get('street_name')
        membership = Membership.objects.get(user=request.user, role='chairman')
        if name:
            Street.objects.create(cooperative=membership.cooperative, name=name)
    return redirect('staff_dashboard')


@login_required
@chairman_required
def edit_street(request, street_id):
    """Зміна назви вулиці"""
    membership = Membership.objects.get(user=request.user, role='chairman')
    street = get_object_or_404(
        Street, id=street_id, cooperative=membership.cooperative)

    if request.method == 'POST':
        new_name = request.POST.get('street_name')
        if new_name:
            street.name = new_name
            street.save()
        return redirect('staff_dashboard')

    return render(request, 'staff/edit_street.html', {'street': street})


@login_required
@chairman_required
def delete_street(request, street_id):
    """Видалення вулиці"""
    membership = Membership.objects.get(user=request.user, role='chairman')
    street = get_object_or_404(
        Street, id=street_id, cooperative=membership.cooperative)

    if request.method == 'POST':
        street.delete()
    return redirect('staff_dashboard')

@login_required
@chairman_required
def voting_list(request):
    """Сторінка для майбутніх голосувань кооперативу"""
    return render(request, 'staff/voting.html')


@login_required
@chairman_required
def edit_member(request, membership_id):
    """Редагування даних мешканця"""
    membership = get_object_or_404(Membership, id=membership_id)
    chairman_mem = Membership.objects.get(user=request.user, role='chairman')

    # Перевірка безпеки: чи належить мешканець до кооперативу цього голови
    if membership.cooperative != chairman_mem.cooperative:
        return redirect('staff_manage')

    if request.method == 'POST':
        user = membership.user
        user.username = request.POST.get('username')
        user.save()

        membership.plot_number = request.POST.get('plot_number')
        street_id = request.POST.get('street')
        if street_id:
            membership.street = Street.objects.get(id=street_id)

        membership.role = request.POST.get('role')
        membership.save()
        return redirect('staff_manage')

    streets = Street.objects.filter(cooperative=chairman_mem.cooperative)
    return render(
        request, 'staff/edit_member.html', {
            'membership': membership,
            'streets': streets
            })


@login_required
@chairman_required
def manage_coop(request):
    """Вивід списку всіх підтверджених мешканців"""
    chairman_mem = Membership.objects.get(user=request.user, role='chairman')
    cooperative = chairman_mem.cooperative

    # Отримуємо всіх членів кооперативу, крім самого голови
    members = Membership.objects.filter(
        cooperative=cooperative
        ).exclude(user=request.user).select_related('user', 'street')

    return render(
        request, 'staff/manage.html', {
            'members': members,
            'cooperative': cooperative
            })


@login_required
@chairman_required
def delete_member(request, membership_id):
    """Метод для видалення мешканця через POST-запит"""
    if request.method == 'POST':
        membership = get_object_or_404(Membership, id=membership_id)
        chairman_mem = Membership.objects.get(
            user=request.user, role='chairman')

        # Перевірка: голова може видаляти лише мешканців свого кооперативу
        if membership.cooperative == chairman_mem.cooperative:
            user_to_delete = membership.user
            user_to_delete.delete()  # Видалення користувача автоматично видаляє його Membership

    return redirect('staff_manage')