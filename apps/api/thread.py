import os
import random
import string
import requests
import json
from django.http import HttpResponse, JsonResponse
from decouple import config
from apps.whatsapp.models import Menu, SubMenu, MenuLink, MenuSession


class ThreadWrapper:
    """class control all the thread in the chatbot"""
    #BASE_URL   = "http://127.0.0.1:8000/"
    BASE_URL   = "http://net.sacids.org/"

    def __init__(self):
        pass


    def call_init_menu(self, **kwargs):
        """ Initialize First Menu Menu """
        phone          = kwargs['phone']
        channel        = kwargs['channel']

        """first menu"""
        menu = Menu.objects.get(flag='Menu_Tukio')

        """random code"""
        uuid = ''.join(random.choices(string.ascii_uppercase, k=12))

        """Create menu session"""
        session_id = self.create_menu_session(phone=phone, menu_id=menu.id, uuid=uuid, channel=channel)

        message = self.process_menu(menu.id, uuid)

        return message


    def check_menu_link(self, menu_id, key):
        """Check Menu Link"""
        sub_menu = SubMenu.objects.filter(menu_id=menu_id)

        if sub_menu.count() > 0:
            sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key).first()

            if (sub_menu_key):
                menu_link = MenuLink.objects.filter(
                    menu_id=menu_id, sub_menu_id=sub_menu_key.id)

                if(menu_link):
                    return 'NEXT_MENU'
                else:
                    return 'INVALID_INPUT'
            else:
                return 'INVALID_INPUT'       
        else:
            menu_link = MenuLink.objects.filter(menu_id=menu_id)

            if(menu_link):
                return 'NEXT_MENU'
            else:
                return 'END_MENU'


    def next_menu(self, **kwargs):
        """Triggering Next Menu"""
        phone       = kwargs['phone']
        uuid        = kwargs['uuid']
        menu_id     = kwargs['menu_id']
        key         = kwargs['key']
        channel     = kwargs['channel']

        """action"""
        action = None

        """sub menu"""
        sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key)

        message = ""
        if (sub_menu_key):
            menu_link = MenuLink.objects.filter(
                menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

            if(menu_link):
                """create menu session"""
                session_id = self.create_menu_session(phone=phone,menu_id=menu_link[0].link_id,uuid=uuid,channel=channel)

                """process menu"""
                message = self.process_menu(menu_link[0].link_id, uuid)

                """menu action"""
                menu = Menu.objects.get(pk=menu_link[0].link_id)

                if menu.action is not None:
                    action = menu.action           
            else:
                """message"""
                message = "Invalid input"
        else:
            menu_link = MenuLink.objects.filter(menu_id=menu_id)

            if(menu_link):
                """create menu session"""
                session_id = self.create_menu_session(phone=phone,menu_id=menu_link[0].link_id,uuid=uuid,channel=channel)

                """process menu"""
                message = self.process_menu(menu_link[0].link_id, uuid)

                """menu action"""
                menu = Menu.objects.get(pk=menu_link[0].link_id)

                if menu.action is not None:
                    action = menu.action
            else:
                """message"""
                message = "Invalid input"

        return JsonResponse({'status': 'success', 'message': message, 'action': action})


    def process_menu(self, menu_id, uuid):
        """Process Menu"""
        message = ""

        menu = Menu.objects.get(pk=menu_id)
        message = menu.title


        if menu.pull == 1:
            """Construct URL"""
            URL = self.BASE_URL + menu.url

            """response"""
            response = requests.get(URL, params={"message_id": uuid})

            sub_message = ""
            for data in response.json()['response']:
                sub_message += data

            message = message + "\r\n" + sub_message  

        elif menu.pull == 0:     
            sub_menus = SubMenu.objects.filter(menu_id=menu_id).order_by('view_id')

            if(sub_menus):
                sub_message = ""
                for val in sub_menus:
                    sub_message += val.view_id + ". " + val.title + "\r\n"

                message = message + "\r\n" + sub_message
        return message 

    
    def create_menu_session(self, **kwargs):
        """create menu session""" 
        phone   = kwargs['phone']
        menu_id = kwargs['menu_id']
        uuid    = kwargs['uuid']
        channel = kwargs['channel']

        """query menu"""
        menu  = Menu.objects.get(pk=menu_id)

        """create menu session"""
        session = MenuSession() 
        session.phone = phone  
        session.code = uuid
        session.menu_id = menu.id
        session.channel = channel
        session.flag = menu.flag
        session.save()

        return session.id


    def process_data(self, **kwargs):
        """Process data for processing"""

        """args"""
        uuid  = kwargs["uuid"]

        """menu sessions"""
        menu_sessions = MenuSession.objects.filter(code=uuid)

        if menu_sessions:
            arr_data = {}
            for menu_session in menu_sessions:
                menu = Menu.objects.get(pk=menu_session.menu_id)
                sub_menu = SubMenu.objects.filter(menu_id=menu.id)

                menu_value = ''
                if sub_menu:
                    sub_menu_value = SubMenu.objects.filter(menu_id=menu.id, view_id=menu_session.values).first()

                    if sub_menu_value:
                        menu_value = sub_menu_value.title
                else:
                    menu_value = menu_session.values

                """assign all data to array"""
                if menu.label is not None and menu_value is not None:
                    arr_data[menu.label] = menu_value

            response = {
                'contents': arr_data, 
                'channel': menu_sessions[0].channel.upper(), 
                'contact': menu_sessions[0].phone
            }

            """response"""
            return response
        else:
            return []