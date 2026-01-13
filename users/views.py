from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from cooperatives.models import Membership, Cooperative
from .forms import CustomUserCreationForm


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    is_chairman = Membership.objects.filter(
        user=request.user, role='chairman').exists()
    if is_chairman:
        return redirect('chairman_dashboard')

    if not request.user.is_approved:
        coop = Cooperative.objects.filter(id=request.user.coop_id).first()
        coop_name = coop.title if coop else "кооперативу"
        return render(
            request, 'registration/pending_approval.html',
            {'coop_name': coop_name})

    return render(request, 'users/dashboard.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False
            user.save()

            coop = Cooperative.objects.filter(id=user.coop_id).first()
            coop_name = coop.title if coop else "кооперативу"

            auth_logout(request)
            return render(
                request, 'registration/pending_approval.html',
                {'coop_name': coop_name})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
