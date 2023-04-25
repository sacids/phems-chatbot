from django.http import JsonResponse
from .models import *
from apps.thread.models import ThreadSession


def get_wards(request):
    """select all wards"""
    wards = Ward.objects.all()

    arr_wards = []
    for ward in wards:
        message = str(ward.view_id) + ". " + ward.name + "\r\n"
        arr_wards.append(message)

    return JsonResponse({"error": False, "response": arr_wards})


def get_villages(request):
    """select all villages based on ward id"""
    messageId   = request.GET.get('message_id')

    """thread session"""
    thread_session = ThreadSession.objects.filter(uuid=messageId).first()

    if thread_session:
        ward_id = thread_session.values
        villages = Village.objects.filter(ward_id=ward_id)
    else:    
        villages = Village.objects.all()

    arr_villages = []
    for village in villages:
        message = str(village.view_id) + ". " + village.name + "\r\n"
        arr_villages.append(message)

    return JsonResponse({"error": False, "response": arr_villages})