import json
import requests
from django.http import HttpResponse, JsonResponse
from decouple import config


class TelegramWrapper:
    API_URL="https://api.telegram.org/bot"
    API_TOKEN=config('TELEGRAM_BOT_TOKEN')

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }

    def get_message_type(self, data):
        """get message type from data"""
        if 'text' in data:
            return 'text'
        elif 'photo' in data:
            return 'photo'
        elif 'location' in data:
            return 'location'  

    def get_message(self, data):
        if 'text' in data:
            return data['text']    

    def send_text_message(self, chat_id, message):
        """__summary__: Send text message """
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        """resposnse"""
        response = requests.request("POST", f"{self.API_URL}{self.API_TOKEN}/sendMessage", data=payload)

        """return response"""
        return response