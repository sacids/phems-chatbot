import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import *
from .utils import *
from .classes import WhatsAppWrapper
from decouple import config

VERIFY_TOKEN = config('FACEBOOK_TOKEN')

#facebook webhooks
@csrf_exempt
def facebook(request):
    """__summary__: Get message from the webhook"""
    if request.method == "GET":
        if request.GET.get('hub.verify_token') == VERIFY_TOKEN:
            return request.GET.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    client = WhatsAppWrapper()

    response = client.process_webhook_notification(request.get_json())
    
    # Do anything with the response
    # Sending a message to a phone number to confirm the webhook is working

    return HttpResponse({"status": "success"}, 200)


@csrf_exempt
def send_template_message(request):
    """__summary__: Send template message"""
    client = WhatsAppWrapper()

    response = client.send_template_message(
        template_name="hello_world",
        language_code="en_US",
        phone_number="255717705746",
    )
    
    return HttpResponse({'error': False, 'response': response})

    
@csrf_exempt
def index(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    """substring phone"""
    phone = user[-13:]

    """check menu session if active=0"""
    menu_session = MenuSession.objects.filter(phone=phone, active=0)

    if menu_session.count() > 0:
        """get latest menu session"""
        m_session = MenuSession.objects.filter(phone=phone, active=0).latest('id')

        """check menu link"""
        menu_response = check_menu_link(m_session.menu_id, message)

        if menu_response == 'NEXT_MENU':
            """update menu session data"""
            m_session.active = 1
            m_session.values = message
            m_session.save()
        
            """call next menu"""
            result = next_menu('whatsapp', phone, m_session.code, m_session.menu_id, message)
            post_data = json.loads(result.content)
            
            """check for post url = None"""
            if(post_data['postURL'] is not None):
                send_data(m_session.code, post_data['postURL'])

        elif menu_response == 'INVALID_INPUT':
            """message for invalid input"""
            result = {'status': 'success', 'message': "Ingizo batili"}
        elif menu_response == 'END_MENU':
            """update menu active = 1"""
            m_session.active = 1
            m_session.save()

            """init menu"""
            result = init_menu('whatsapp', phone)   
    else:  
        if message.upper() == "START" or message.upper() == "ANZA":
            result = init_menu('whatsapp', phone)
        else:
            result = {'status': 'success', 'message': "Anzisha OHD chat ukitumia neno kuu START au ANZA"}

        """init first menu"""
        
    """data formarting"""
    data = json.loads(result.content)

    """response"""
    response = MessagingResponse()
    response.message(data['message']) 

    return HttpResponse(str(response))


"""privacy policy"""
def privacy_policy(request):
    return render(request, "html/index.html", {})




