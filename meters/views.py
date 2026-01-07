from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Meter
from django.shortcuts import redirect, get_object_or_404
from .forms import ReadingForm  # Не забудь імпортувати форму!

@login_required
def dashboard(request):
    # 1. Знаходимо всі лічильники, які належать поточному юзеру
    # Ми шукаємо лічильники, де membership -> user == request.user (той, хто зайшов)
    my_meters = Meter.objects.filter(membership__user=request.user)

    context = {
        'meters': my_meters,
        'user': request.user
        }

    # 2. Віддаємо ці дані в HTML-шаблон
    return render(request, 'meters/dashboard.html', context)

@login_required
def submit_reading(request, meter_id):
    # Спочатку перевіряємо, чи має право цей юзер чіпати цей лічильник
    meter = get_object_or_404(Meter, id=meter_id, membership__user=request.user)

    # ОСЬ ТУТ ЛОВИМО POST-ЗАПИТ!
    if request.method == 'POST':
        # Заповнюємо форму даними, які прийшли від користувача
        form = ReadingForm(request.POST, request.FILES)
        if form.is_valid():
            # Якщо дані правильні — зберігаємо
            reading = form.save(commit=False)
            reading.meter = meter
            reading.submitted_by = request.user
            reading.save()
            # І перекидаємо назад в кабінет
            return redirect('dashboard')
    else:
        # Якщо це не POST, а просто відкрили сторінку — показуємо пусту форму
        form = ReadingForm()

    return render(request, 'meters/submit_reading.html', {'form': form, 'meter': meter})