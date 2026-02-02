from django.http import JsonResponse
from .models import Cooperative


def check_coop_id(request):

    coop_id = request.GET.get('coop_id', None)
    cooperative = Cooperative.objects.filter(id=coop_id).first()
    if cooperative:
        streets = list(cooperative.street_set.values_list('name', flat=True))

        return JsonResponse(
            {
                'exists': True,
                'name': cooperative.title,
                'streets': streets
                })

    return JsonResponse({'exists': False})
