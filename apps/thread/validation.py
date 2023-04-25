from django.http import JsonResponse
from apps.setup.models import *
from apps.thread.models import *


def validate_village(request):
    """validate village """
    village_name = request.GET.get('key')

    """query from village"""
    village = Village.objects.filter(dictionary__icontains=village_name)

    if village.count() > 0:
        if village.count() == 1:
            """validation True"""
            return JsonResponse({'error': False, 'validation': True, 'data': 'NEXT_MENU', 'value': village[0].name})
        elif village.count() > 1:
            """validation False"""
            return JsonResponse({'error': True, 'validation': False, 'data': 'WARD_MENU', 'value': village[0].name})
    else:
        """Invalid input"""
        return JsonResponse({'error': True, 'validation': False, 'data': 'INVALID_INPUT'})

        
def validate_ward(request):
    """validate ward """
    uuid        = request.GET.get('uuid')
    ward_name   = request.GET.get('key')

    """query for wards"""
    ward = Ward.objects.filter(dictionary__icontains=ward_name)

    if ward.count() > 0:
        if ward.count() == 1:
            village_thread = Thread.objects.filter(flag='Thread_Kijiji').first()

            """GET data from previous thread"""
            thread_session = ThreadSession.objects.filter(thread_id=village_thread.id, uuid=uuid).first()
        
            """ward village"""
            ward_village = Ward.objects.prefetch_related('village').filter(village__name=thread_session.values, name=ward[0].name)
        
            """validation True"""
            return JsonResponse({'error': False, 'validation': True, 'data': 'NEXT_MENU', 'value': ward_village[0].name})     
        elif ward.count() > 1:
            """TODO: Move to district thread"""
            pass
    else:
        """Invalid input"""
        return JsonResponse({'error': True, 'validation': False, 'data': 'INVALID_INPUT'})





