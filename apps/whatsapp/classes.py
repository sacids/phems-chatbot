import os
import requests
import json
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


    def process_webhook_notification(self, data):
        """_summary_: Process webhook notification
        For the moment, this will return the type of notification
        """

        response = []

        for entry in data["entry"]:

            for change in entry["changes"]:
                response.append(
                    {
                        "type": change["field"],
                        "from": change["value"]["metadata"]["display_phone_number"],
                    }
                )
        # Do whatever with the response
        return response