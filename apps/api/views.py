import requests
import json
from django.http import HttpResponse
from apps.whatsapp.utils import *
from django.db.models import Max

API_BASE_URL = 'https://dev.sacids.org'

#sending data
def send_data(request):
    menu_sessions = MenuSession.objects.filter(sent=0).values("code").annotate(Max('id'))

    for val in menu_sessions:
        #process data
        payload = process_data(val['code'])

        #post data
        response = requests.post(f"{API_BASE_URL}/ems/api/signal/", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
        print(response.json())

        #update sent = 1
        MenuSession.objects.filter(code=val['code']).update(sent=1)
        
    #browser response
    return HttpResponse(str('success =>  data sent!'))
