import json
import logging
import requests
from decouple import config
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.whatsapp.models import *
from .classes import TelegramWrapper
from apps.api.thread import ThreadWrapper

TELEGRAM_URL="https://api.telegram.org/bot"
BOT_TOKEN=config('TELEGRAM_BOT_TOKEN')

# Create your views here.
@csrf_exempt
def index(request):
    """__summary__: Get message from the webhook"""
    client = TelegramWrapper()

    """data from Telegram"""
    t_data = json.loads(request.body)
    t_message = t_data["message"]
    t_chat = t_message["chat"]

    print(f'telegram bot says {t_message}')
    
    """message type"""
    message_type = client.get_message_type(t_message)

    if message_type == 'text':
        message = client.get_message(t_message)
        from_number = t_chat["id"]

        """process thread"""
        new_message = process_threads(from_number=from_number, key=message)

        """send message"""
        response = client.send_text_message(from_number, new_message)

    """return response"""
    return JsonResponse({"ok": "POST request processed"})


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
            result = thread.next_menu(phone=from_number, uuid=OD_uuid, menu_id=OD_menu_id, key=key, channel="telegram")
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
            message = thread.call_init_menu(phone=from_number, channel="telegram") 
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
