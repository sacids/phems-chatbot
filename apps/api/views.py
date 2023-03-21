import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    """__summary__: Get data from the eGA USSD"""


    """data from Telegram"""
    t_data = json.loads(request.body)
    text = t_data["menu_tukio"]
    village = t_data[""]

    # 'text' => $value['menu_tukio'],
    #         'village' => $value['tukio_kijiji'],
    #         'ward' => $value['tukio_kata']

    # print(f'telegram bot says {t_message}')
