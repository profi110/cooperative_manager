from django.shortcuts import render, redirect
from .forms import CooperativeApplicationForm


def register_cooperative(request):
    if request.method == 'POST':
        form = CooperativeApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'cooperatives/application_success.html')
    else:
        form = CooperativeApplicationForm()

    return render(
        request, 'cooperatives/register_cooperative.html', {'form': form})