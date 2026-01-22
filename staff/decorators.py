from django.shortcuts import redirect
from cooperatives.models import Membership

def chairman_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            is_chairman = Membership.objects.filter(user=request.user, role='chairman').exists()
            if is_chairman:
                return view_func(request, *args, **kwargs)
        return redirect('user_dashboard')
    return _wrapped_view