from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Meter
from django.shortcuts import redirect, get_object_or_404
from .forms import ReadingForm


@login_required
def submit_reading(request, meter_id):
    meter = get_object_or_404(Meter, id=meter_id, membership__user=request.user)

    if request.method == 'POST':
        form = ReadingForm(request.POST, request.FILES)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.meter = meter
            reading.submitted_by = request.user
            reading.save()
            return redirect('dashboard')
    else:
        form = ReadingForm()

    return render(request, 'meters/submit_reading.html', {'form': form, 'meter': meter})