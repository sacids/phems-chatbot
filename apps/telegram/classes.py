import requests
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
        """get message text from the data"""
        if 'text' in data:
            return data['text']  

    def get_location(self, data):
        """get location from the data"""

        if "location" in data:
            return data["location"]

    def get_image(self, data):
        """get image from the data"""
        
        if "photo" in data:
            return data["photo"]

    def query_media_url(self, media_id):
        """Query media url from media id obtained either by manually uploading media or received media"""
        response = requests.get(f"{self.API_URL}{self.API_TOKEN}/getFile?file_id={media_id}", headers=self.headers)
        response = response.json()
        
        if response['ok'] == "true":
            fileURL = response['result']['file_path']
            return fileURL
        return None

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