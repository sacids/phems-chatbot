import json
import requests
from django.http import HttpResponse, JsonResponse
from decouple import config


class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v15.0/"
    API_TOKEN=config('WHATSAPP_API_TOKEN')
    NUMBER_ID=config('WHATSAPP_NUMBER_ID')

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID


    def preprocess(self, data):
        """Preprocess data"""
        return data["entry"][0]["changes"][0]["value"]   


    def get_mobile(self, data):
        """get mobile from the data"""
        data = self.preprocess(data)

        if "contacts" in data:
            return data['contacts'][0]['wa_id'] 

    def get_profile_name(self, data):
        """get profile data from the data"""
        data = self.preprocess(data)

        if "contacts" in data:
            return data['contacts'][0]['profile']['name'] 

    def get_message(self, data):
        """get message from the data""" 
        data = self.preprocess(data)

        if 'messages' in data:
            return data['messages'][0]['text']['body']

    def get_messageId(self, data):
        """get message id from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['id']  

    def get_message_timestamp(self, data):
        """get message timestamp from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['timestamp']                  

    def get_message_type(self, data):
        """get message type from data"""
        data = self.preprocess(data) 

        if 'messages' in data:
            return data['messages'][0]['type']  

    def get_delivery(self, data):
        """get message type from data"""
        data = self.preprocess(data) 

        if 'statuses' in data:
            return data['statuses'][0]['status']              


    def send_template_message(self, template_name, language_code, phone_number):
        """__summary__: Send templete message """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        """return response"""
        return response

    def send_text_message(self, phone_number, message):
        """__summary__: Send templete message """
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        """return response"""
        return response