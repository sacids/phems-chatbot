import json
import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import *
from .utils import *
from .classes import WhatsAppWrapper
from apps.api.thread import ThreadWrapper
from decouple import config

VERIFY_TOKEN = config('FACEBOOK_TOKEN')

@csrf_exempt
def verification(request):
    """__summary__: verification of webhook"""
    if request.method == "GET":
        if request.GET.get('hub.verify_token') == VERIFY_TOKEN:
            return request.GET.get('hub.challenge')
        return "Authentication failed. Invalid Token."
    
    # Do anything with the response
    # Sending a message to a phone number to confirm the webhook is working

    return HttpResponse({"status": "success"}, 200)

@csrf_exempt
def webhook(request):
    """__summary__: Get message from the webhook"""
    client = WhatsAppWrapper()

    data = request.get_json()
    logging.info("Received webhook data: %s", data)

    """extract => field, from, key, message_type"""
    field = data["entry"][0]["changes"][0]["field"]

    """check if field not messages and reply 400 response"""
    if field != 'messages':
        return HttpResponse(400)

    """new message"""
    new_message = client.get_mobile(data)

    if new_message:
        from_number = client.get_mobile(data)
        profile_name = client.get_profile_name(data)
        message_type = client.get_message_type(data)
        timestamp = client.get_message_timestamp(data)
        facebook_id = client.get_messageId(data)

        if message_type == 'text':
            message = client.get_message(data)

            """process thread"""
            new_message = process_threads(from_number=from_number, key=message)

            """send message"""
            response = client.send_text_message(from_number, new_message)
    else:
        delivery = client.get_delivery(data)
        if delivery:
            print(f"Message : {delivery}")
        else:
            print("No new message")

    """return response to facebook"""
    return request.get_json()

def process_threads(**kwargs):
    """process all the threads"""
    from_number = kwargs['from_number']
    key         = kwargs['key']

    """initiate message"""
    message = ""

    """thread wrapper"""
    thread = ThreadWrapper()

    """Follow menu session and Trigger follow up menu"""
    menu_session = MenuSession.objects.filter(phone=from_number, active=0) 

    if menu_session.count() > 0:
        m_session = MenuSession.objects.filter(phone=from_number, active=0).latest('id')
        menu_response = thread.check_menu_link(m_session.menu_id, key) 

        if menu_response == 'NEXT_MENU':
            """update menu session"""
            m_session.active = 1
            m_session.values = key
            m_session.save()

            """update data """
            OD_uuid = m_session.code
            OD_menu_id = m_session.menu_id

            """result"""
            result = thread.next_menu(phone=from_number, uuid=OD_uuid, menu_id=OD_menu_id, key=key, channel="whatsapp")
            data = json.loads(result.content)

            """message"""
            message = data['message']

            """check for action = None"""
            if(data['action'] is not None):
                if data['action'] == 'create':
                    """update all menu session"""
                    m_session.active = 1
                    m_session.save()

                    """process data"""
                    response = thread.process_data(uuid=OD_uuid)
                    my_data = json.loads(response.content)
                    print(my_data)
                    result = push_data(payload=my_data)

        elif menu_response == 'INVALID_INPUT':
            """invalid input"""
            message = "Chagua batili, tafadhali chagua tena!"

        elif menu_response == 'END_MENU':
            """update and end menu session"""
            m_session.active = 1
            m_session.save()

            """initiate menu session"""
            message = "Asante kwa kukamilisha usajili wako!"    
    else:
        if key.upper() == "START" or key.upper() == "ANZA":
            """initiate menu session"""
            message = thread.call_init_menu(phone=from_number, channel="whatsapp") 
        else:
            message = "Anzisha OHD chat ukitumia neno kuu START au ANZA"    

    """return message"""
    return message


def push_data(**kwargs):
    """push data to external API"""
    payload = kwargs['payload']

    """base url"""
    baseURL = "https://dev.sacids.org/ems/api/signal/"

    """push data"""
    response = requests.post(f"{baseURL}", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    print(response.json())
        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})


"""privacy policy"""
def privacy_policy(request):
    return render(request, "html/index.html", {})




