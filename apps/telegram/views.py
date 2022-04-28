import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.whatsapp.models import *

TELEGRAM_URL="https://api.telegram.org/bot"
BOT_TOKEN="5210813918:AAEB0WKoRdQ8R3dMPVYXNmnS-4HwhtG8Ov4"

# Create your views here.
@csrf_exempt
def index(request):
    t_data = json.loads(request.body)
    t_message = t_data["message"]
    t_chat = t_message["chat"]
    print(f'telegram bot says {t_message}')

    #menu session
    menu_session = MenuSession.objects.filter(message_id=t_chat["id"], active=0)

    if menu_session.count() > 0:
        # get latest menu session
        m_session = MenuSession.objects.filter(message_id=t_chat["id"], active=0).latest('id')

        #check if input == text,photo,video
        if 'text' in t_message:
            message = t_message['text']
        elif 'photo' in t_message:
            message = t_message['photo']    

        #check menu link
        menu_response = check_menu_link(m_session.menu_id, message)

        if menu_response == 'NEXT_MENU':
            #update menu session data
            m_session.active = 1
            m_session.values = message
            m_session.save()
        
            #call next menu
            result = next_menu('telegram', t_chat["id"], m_session.code, m_session.menu_id, message)
        elif menu_response == 'INVALID_INPUT':
            #message for invalid input
            result = {'status': 'success', 'message': "Invalid input"}
        elif menu_response == 'END_MENU':
            #update menu active = 1
            m_session.active = 1
            m_session.save()

            #init menu
            result = init_menu('telegram', t_chat["id"])  
    else:
        #init first menu
        result = init_menu('telegram', t_chat["id"])

    #data json
    data = json.loads(result.content)

    # send sms
    send_message(data['message'], t_chat["id"])

    # response
    return JsonResponse({"ok": "POST request processed"})

#send message
def send_message(message, chat_id):
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)
