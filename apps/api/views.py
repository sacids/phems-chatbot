import requests
import json
from django.http import HttpResponse
from apps.whatsapp.models import *
from django.db.models import Max

BASE_URL = 'http://41.73.194.139:8000'

#sending data
def send_data(request):
    menu_sessions = MenuSession.objects.filter(sent=0).values("code").annotate(Max('id'))

    for val in menu_sessions:
        #process data
        payload = process_data(val['code'])

        #post data
        post_url = BASE_URL + '/ems/api/signal/'
        headers = {"Content-Type": "application/json; charset=utf-8"}

        response = requests.post(post_url, data = json.dumps(payload), headers=headers)
        print(response.json)

        #update sent = 1
        MenuSession.objects.filter(code=val['code']).update(sent=1)
        
    #browser response
    return HttpResponse(str('success =>  data sent!'))
