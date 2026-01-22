from cooperatives.models import Membership

def chairman_status(request):
    if request.user.is_authenticated:
        # Перевіряємо, чи є користувач головою хоча б в одному кооперативі
        is_chairman = Membership.objects.filter(user=request.user, role='chairman').exists()
        return {'is_chairman': is_chairman}
    return {'is_chairman': False}