from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cooperative, Street, Membership
from users.models import CustomUser

def check_coop_id(request):
    coop_id = request.GET.get('coop_id', None)
    cooperative = Cooperative.objects.filter(id=coop_id).first()
    if cooperative:
        streets = list(cooperative.street_set.values_list('name', flat=True))
        return JsonResponse({'exists': True, 'name': cooperative.title, 'streets': streets})
    return JsonResponse({'exists': False})

@login_required
def chairman_dashboard(request):
    membership = Membership.objects.filter(user=request.user, role='chairman').first()
    if not membership:
        return render(request, 'errors/403.html', {'message': "Ви не голова"})

    pending_residents = CustomUser.objects.filter(coop_id=str(membership.cooperative.id), is_approved=False)
    return render(request, 'cooperatives/chairman_dashboard.html', {
        'cooperative': membership.cooperative,
        'residents': pending_residents
    })

@login_required
def add_street(request):
    membership = Membership.objects.filter(user=request.user, role='chairman').first()
    if request.method == 'POST' and membership:
        street_name = request.POST.get('street_name')
        if street_name:
            Street.objects.create(name=street_name, cooperative=membership.cooperative)
    return redirect('chairman_dashboard')

@login_required
def delete_street(request, street_id):
    membership = Membership.objects.filter(user=request.user, role='chairman').first()
    if membership:
        street = get_object_or_404(Street, id=street_id, cooperative=membership.cooperative)
        street.delete()
    return redirect('chairman_dashboard')

@login_required
def approve_resident(request, user_id):
    is_chairman = Membership.objects.filter(user=request.user, role='chairman').exists()
    if is_chairman:
        resident = get_object_or_404(CustomUser, id=user_id)
        resident.is_approved = True
        resident.save()
    return redirect('chairman_dashboard')

def register_cooperative(request):
    return render(request, 'cooperatives/register_cooperative.html')
