import os
import random
import string
import requests
import json
from django.http import HttpResponse, JsonResponse
from .models import *

class ThreadWrapper:
    """class control all the thread in the chatbot"""
    #BASE_URL   = "http://127.0.0.1:8000/"
    BASE_URL   = "https://net.sacids.org/"

    def __init__(self):
        pass


    def init_thread(self, **kwargs):
        """ Initialize first thread """
        phone          = kwargs['phone']
        channel        = kwargs['channel']

        """first thread"""
        thread = Thread.objects.get(flag='Thread_Service')

        """random code"""
        uuid = ''.join(random.choices(string.ascii_uppercase, k=12))

        """Create menu session"""
        session_id = self.create_thread_session(phone=phone, thread_id=thread.id, uuid=uuid, channel=channel)

        message = self.process_thread(thread.id, uuid)

        return message


    def check_thread_link(self, thread_id, key):
        """Check Thread Link"""
        sub_thread = SubThread.objects.filter(thread_id=thread_id)

        if sub_thread.count() > 0:
            sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key).first()

            if (sub_thread_key):
                thread_link = ThreadLink.objects.filter(
                    thread_id=thread_id, sub_thread_id=sub_thread_key.id)

                if(thread_link):
                    return 'NEXT_MENU'
                else:
                    return 'INVALID_INPUT'
            else:
                return 'INVALID_INPUT'       
        else:
            thread_link = ThreadLink.objects.filter(thread_id=thread_id)

            if(thread_link):
                return 'NEXT_MENU'
            else:
                return 'END_MENU'


    def next_thread(self, **kwargs):
        """Triggering Next Thread"""
        phone       = kwargs['phone']
        uuid        = kwargs['uuid']
        thread_id   = kwargs['thread_id']
        key         = kwargs['key']
        channel     = kwargs['channel']

        """action"""
        action = None
        action_url = None

        """sub thread"""
        sub_thread_key = SubThread.objects.filter(thread_id=thread_id, view_id=key)

        message = ""
        if (sub_thread_key):
            thread_link = ThreadLink.objects.filter(
                thread_id=thread_id, sub_thread_id=sub_thread_key[0].id)

            if(thread_link):
                """create session"""
                session_id = self.create_thread_session(phone=phone, thread_id=thread_link[0].link_id, uuid=uuid, channel=channel)

                """process thread"""
                message = self.process_thread(thread_link[0].link_id, uuid)

                """thread action"""
                thread = Thread.objects.get(pk=thread_link[0].link_id)

                if thread.action is not None:
                    action = thread.action           
                    action_url = thread.action_url           
            else:
                """message"""
                message = "Invalid input"
        else:
            thread_link = ThreadLink.objects.filter(thread_id=thread_id)

            if(thread_link):
                """create session"""
                session_id = self.create_thread_session(phone=phone, thread_id=thread_link[0].link_id, uuid=uuid, channel=channel)

                """process thread"""
                message = self.process_thread(thread_link[0].link_id, uuid)

                """thread action"""
                thread = Thread.objects.get(pk=thread_link[0].link_id)

                if thread.action is not None:
                    action = thread.action
                    action_url = thread.action_url  
            else:
                """message"""
                message = "Invalid input"

        """return response"""
        return JsonResponse({'status': 'success', 'message': message, 'action': action, 'action_url': action_url})


    def process_thread(self, thread_id, uuid):
        """Process Thread"""
        message = ""

        """Query Thread"""
        thread = Thread.objects.get(pk=thread_id)
        message = thread.title

        if thread.pull == 1:
            """Construct URL"""
            URL = self.BASE_URL + thread.url

            """response"""
            response = requests.get(URL, params={"message_id": uuid})

            sub_message = ""
            for data in response.json()['response']:
                sub_message += data

            message = message + "\r\n" + sub_message  

        elif thread.pull == 0:     
            sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

            if(sub_threads):
                sub_message = ""
                for val in sub_threads:
                    sub_message += val.view_id + ". " + val.title + "\r\n"

                message = message + "\r\n" + sub_message

        """Return message"""        
        return message 

    
    def create_thread_session(self, **kwargs):
        """create menu session""" 
        phone   = kwargs['phone']
        thread_id = kwargs['thread_id']
        uuid    = kwargs['uuid']
        channel = kwargs['channel']

        """query thread"""
        thread  = Thread.objects.get(pk=thread_id)

        """create  new session"""
        session = ThreadSession()
        session.phone = phone  
        session.uuid = uuid
        session.thread_id = thread_id
        session.channel = channel
        session.flag = thread.flag
        session.save()

        return session.id


    def process_data(self, **kwargs):
        """Process data for processing"""
        uuid  = kwargs["uuid"]

        """thread sessions"""
        thread_sessions = ThreadSession.objects.filter(uuid=uuid)

        if thread_sessions:
            arr_data = {}
            for t_session in thread_sessions:
                thread = Thread.objects.get(pk=t_session.thread_id)
                sub_thread = SubThread.objects.filter(thread_id=thread.id)

                thread_value = ''
                if sub_thread:
                    sub_thread_value = SubThread.objects.filter(thread_id=thread.id, view_id=t_session.values).first()

                    if sub_thread_value:
                        thread_value = sub_thread_value.title
                else:
                    thread_value = t_session.values

                """assign all data to array"""
                if thread.label is not None and thread_value is not None:
                    arr_data[thread.label] = thread_value

            response = {
                'contents': arr_data, 
                'channel': thread_sessions[0].channel.upper(), 
                'contact': thread_sessions[0].phone
            }

            """response"""
            return response
        else:
            return []