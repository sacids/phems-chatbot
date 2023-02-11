import json
import logging
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .classes import WhatsAppWrapper
from apps.thread.classes import ThreadWrapper
from apps.thread.models import *
from decouple import config

VERIFY_TOKEN = config('WHATSAPP_VERIFY_TOKEN')
API_URL = "https://graph.facebook.com/v15.0/"


def testing(request):
    """message"""
    message = request.GET.get('message')
    from_number = request.GET.get('from_number')

    print("key => " + message)
    print("from number => " + from_number)

    """process thread"""
    new_message = process_threads(from_number=from_number, key=message)

    """return response to telerivet"""
    return HttpResponse(json.dumps({
        'messages': [
            {"content": new_message}
        ]
    }), 'application/json') 


@csrf_exempt
def facebook(request):
    """__summary__: Get message from the webhook"""
    wrapper = WhatsAppWrapper()

    if request.method == "GET":
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status = 200)
        else:
            return HttpResponse('Authentication failed. Invalid Token.', status=403)    


    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        """extract => field, from, key, message_type"""
        field = data["entry"][0]["changes"][0]["field"]

        """check if field not messages and reply 400 response"""
        if field != 'messages':
            return HttpResponse('Invalid data', 400)

        """new message"""
        new_message = wrapper.get_mobile(data)

        if new_message:
            from_number = wrapper.get_mobile(data)
            profile_name = wrapper.get_profile_name(data)
            message_type = wrapper.get_message_type(data)
            timestamp = wrapper.get_message_timestamp(data)
            facebook_id = wrapper.get_messageId(data)

            if message_type == 'text':
                message = wrapper.get_message(data)

                """process thread"""
                new_message = process_threads(from_number=from_number, key=message)

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)

            elif message_type == 'location':
                message_location = wrapper.get_location(data)

                """latitude and longitude"""
                latitude     = message_location["latitude"]
                longitude    = message_location["longitude"]
                new_location = f"{latitude} {longitude}"

                """process thread"""
                new_message = process_threads(from_number=from_number, key=new_location)

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)

            elif message_type == 'image':
                image = wrapper.get_image(data)  

                """get image data"""
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = wrapper.query_media_url(image_id)
  
                print("image URL")
                print(image_url)

                """TODO: save image to a folder"""

                """process thread"""
                new_message = process_threads(from_number=from_number, key=image_url)

                """send message"""
                response = wrapper.send_text_message(from_number, new_message)
        else:
            delivery = wrapper.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")

        """return response"""
        return HttpResponse('success', status=200)    


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
            result = client.next_thread(phone=from_number, uuid=OD_uuid, thread_id=OD_thread_id, key=key, channel="WHATSAPP")
            data = json.loads(result.content)

            """message"""
            message = data['message']

            """check for action = None"""
            if(data['action'] is not None):
                """update all menu session"""
                ThreadSession.objects.filter(uuid=OD_uuid).update(active=1)

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
        if key.upper() == "START" or key.upper() == "ANZA":
            """initiate thread session"""
            message = client.init_thread(phone=from_number, channel="WHATSAPP") 
        else:
            message = "Anzisha OHD Chatbot ukitumia neno kuu START au ANZA"    

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


"""privacy policy"""
def privacy_policy(request):
    return render(request, "html/index.html", {})




