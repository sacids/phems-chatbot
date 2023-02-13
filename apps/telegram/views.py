import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .classes import TelegramWrapper
from apps.thread.classes import ThreadWrapper
from apps.thread.models import *


# Create your views here.
@csrf_exempt
def index(request):
    """__summary__: Get message from the webhook"""
    wrapper = TelegramWrapper()

    """data from Telegram"""
    t_data = json.loads(request.body)
    t_message = t_data["message"]
    t_chat = t_message["chat"]

    print(f'telegram bot says {t_message}')
    
    """message type"""
    message_type = wrapper.get_message_type(t_message)

    if message_type == 'text':
        message = wrapper.get_message(t_message)
        from_number = t_chat["id"]

        """process thread"""
        new_message = process_threads(from_number=from_number, key=message)

        """send message"""
        response = wrapper.send_text_message(from_number, new_message)

    elif message_type == 'photo':
        photo = wrapper.get_image(t_message)  
        from_number = t_chat["id"]

        """get image data"""
        image_id = photo[0]["file_id"]
        image_url = wrapper.query_media_url(image_id)

        print("image URL")
        print(image_url)

        """TODO: save image to a folder"""

        """process thread"""
        new_message = process_threads(from_number=from_number, key=image_url)

        """send message"""
        response = wrapper.send_text_message(from_number, new_message)

    """return response"""
    return JsonResponse({"ok": "POST request processed"})


def process_threads(**kwargs):
    """process all the threads"""
    from_number = kwargs['from_number']
    key         = kwargs['key']

    """initiate message"""
    message = ""

    """thread wrapper"""
    client = ThreadWrapper()

    """Follow thread session and Trigger follow up menu"""
    thread_session = ThreadSession.objects.filter(phone=from_number, active=0) 

    if thread_session.count() > 0:
        m_session = ThreadSession.objects.filter(phone=from_number, active=0).latest('id')
        thread_response = client.check_thread_link(m_session.thread_id, key) 

        if thread_response == 'NEXT_MENU':
            """update thread session"""
            m_session.active = 1
            m_session.values = key
            m_session.save()

            """update data """
            OD_uuid = m_session.uuid
            OD_thread_id = m_session.thread_id

            """result"""
            result = client.next_thread(phone=from_number, uuid=OD_uuid, thread_id=OD_thread_id, key=key, channel="TELEGRAM")
            data = json.loads(result.content)

            """message"""
            message = data['message']

            """check for action = None"""
            if(data['action'] is not None):
                """update all menu session"""
                m_session.active = 1
                m_session.save()
                #ThreadSession.objects.filter(uuid=OD_uuid).update(active=1)

                """process data"""
                response = client.process_data(uuid=OD_uuid)
                my_data = json.loads(response.content)
                print(my_data)

                if data['action'] == 'PUSH':
                    """push data"""
                    result = push_data(payload=my_data, action_url=data['action_url'])

        elif thread_response == 'INVALID_INPUT':
            """invalid input"""
            message = "Chaguo batili, tafadhali chagua tena!"

        elif thread_response == 'END_MENU':
            """update and end thread session"""
            m_session.active = 1
            m_session.save()

            """initiate thread session"""
            message = "Asante kwa kuripoti taarifa!"    
    else:
        if key.upper() == "TAARIFA" or key.upper() == "ANZA":
            """initiate thread session"""
            message = client.init_thread(phone=from_number, channel="TELEGRAM") 
        else:
            message = "Ripoti taarifa za matukio kwa OHD Chatbot kwa kutuma neno TAARIFA au ANZA"    

    """return message"""
    return message


def push_data(**kwargs):
    """push data to external API"""
    payload   = kwargs['payload']
    actionURL = kwargs['action_url']

    """push data"""
    response = requests.post(f"{actionURL}", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    print(response.json())
        
    """response"""
    return JsonResponse({'status': 'success', 'message': "data sent"})
