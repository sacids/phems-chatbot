import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from django.db.models import Max
from .models import *

# Create your views here.
@csrf_exempt
def index(request):
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

        #check menu link
        menu_response = check_menu_link(m_session.menu_id, message)

        if menu_response == 'NEXT_MENU':
            #update menu session data
            m_session.active = 1
            m_session.values = message
            m_session.save()
        
            #call next menu
            result = next_menu('whatsapp', phone, m_session.code, m_session.menu_id, message)
        elif menu_response == 'INVALID_INPUT':
            #message for invalid input
            result = {'status': 'success', 'message': "Invalid input"}
        elif menu_response == 'END_MENU':
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


#sending data
def send_data(request):
    menu_sessions = MenuSession.objects.filter(sent=0).values("code").annotate(Max('id'))

    for val in menu_sessions:
        #process data
        data = process_data(val['code'])
        post_url = '/ems/signal/'

        #post data
        response = requests.post(post_url, data = data)
        print(response)

        #todo: update sent = 1

    #browser response
    return HttpResponse(str('success =>  data sent!'))
