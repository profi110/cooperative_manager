from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# 👇 Переконайтеся, що у вас у meters/forms.py клас називається саме ReadingForm!
from meters.forms import ReadingForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ReadingForm(request.POST, request.FILES)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            return redirect('user_dashboard')
        else:
            print("🛑 ПОМИЛКИ ФОРМИ:", form.errors)
    else:
        form = ReadingForm()

    return render(request, 'users/dashboard.html', {'form': form})