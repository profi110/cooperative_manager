from django.shortcuts import redirect
from django.contrib import messages
from cooperatives.models import Membership


def chairman_required(view_func):
    """Декоратор: доступ лише для Голови"""

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        membership = Membership.objects.filter(user=request.user).first()

        if membership and membership.role == 'chairman':
            return view_func(request, *args, **kwargs)

        if membership and membership.role == 'accountant':
            messages.warning(
                request, "У вас немає прав для доступу до цього розділу.")
            return redirect('staff_dashboard')

        return redirect('user_dashboard')

    return _wrapped_view


def staff_required(view_func):
    """Декоратор: доступ для персоналу (Голова + Бухгалтер)"""

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        is_staff = Membership.objects.filter(
            user=request.user,
            role__in=['chairman', 'accountant']
            ).exists()

        if is_staff:
            return view_func(request, *args, **kwargs)

        return redirect('user_dashboard')

    return _wrapped_view
