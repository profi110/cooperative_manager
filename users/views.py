from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Переконайся, що forms.py існує!

# Головна сторінка (Landing Page)
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

# 👇 ОСЬ ЦІЄЇ ФУНКЦІЇ НЕ ВИСТАЧАЛО
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})