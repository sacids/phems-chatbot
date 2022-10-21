import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import *
from .utils import *

ACCESS_TOKEN ='EAAFLn31liucBAIVv3Mlf9lXYNYAPyfUv32yyuoySP5QkZAWrSiYM9ZB0IabvBrKvEYvXesgoCUXBoNqKZAXAEpYlUS7MUEdDelce6H2tZBi2a2pgRkvxfeQTFH7p3YjICr34TIbzHZBiZBDwNJh9XQ1aMj0oZBZBSKIT6ZBck2o2mOO70H7Yvupst'


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
            post_data = json.loads(result.content)
            
            #check for post url = None
            if(post_data['postURL'] is not None):
                send_data(m_session.code, post_data['postURL'])

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
