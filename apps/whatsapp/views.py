import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import *

# Create your views here.
@csrf_exempt
def message(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    # substring phone
    phone = user[-12:]

    #check menu session if active=0
    menu_session = MenuSession.objects.filter(phone=phone, active=0)

    if menu_session.count() > 0:
        # get latest menu session
        m_session = MenuSession.objects.filter(phone=phone, active=0).latest('id')

        if check_menu_link(m_session.menu_id, message):
            #update menu session data
            m_session.active = 1
            m_session.values = message
            m_session.save()
        
            #call next menu
            result = next_menu('whatsapp', phone, m_session.code, m_session.menu_id, message)
        else:
            #update menu active = 1
            m_session.active = 1
            m_session.save()

            #init menu
            result = init_menu('whatsapp', phone)
    else:
        #init first menu
        result = init_menu('whatsapp', phone)

    #data json
    data = json.loads(result.content)

    # response
    response = MessagingResponse()
    response.message(data['message']) 

    #return
    return HttpResponse(str(response))