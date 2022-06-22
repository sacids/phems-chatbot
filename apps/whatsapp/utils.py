import random
import string
import json
import requests
from django.http import JsonResponse
from .models import *

#init menu
def init_menu(channel, phone):
    # get first menu
    menu = Menu.objects.get(flag='Menu_Tukio')

    #generate random key
    random_code = ''.join(random.choices(string.ascii_uppercase, k=12))

    # create menu session
    session = MenuSession()
    session.channel = channel    
    session.code = random_code
    session.menu_id = menu.id

    #check for channel
    if(channel == 'whatsapp'):
        session.phone = phone
    elif(channel == 'telegram'):
        session.message_id = phone

    #save
    session.save()

    # process menu
    message = process_menu(menu_id=menu.id)

    # response
    return JsonResponse({'status': 'success', 'message': message})

#provess menu
def process_menu(menu_id):
    # variables
    message = ''

    # get menu
    menu = Menu.objects.get(pk=menu_id)
    message = menu.title

    # get sub menu
    sub_menus = SubMenu.objects.filter(menu_id=menu_id).order_by('view_id')

    if(sub_menus):
        sub_message = ''
        for val in sub_menus:
            sub_message += val.view_id + ". " + val.title + "\r\n"

        message = message + "\r\n" + sub_message

    # response
    return message    

#check if there menu links
def check_menu_link(menu_id, key):
    sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id= key)

    if (sub_menu_key):
        menu_link = MenuLink.objects.filter(
            menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

        if(menu_link):
            return 'NEXT_MENU'
        else:
            return 'INVALID_INPUT'
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            return 'NEXT_MENU'
        else:
            return 'END_MENU'

#next menu
def next_menu(channel, phone, uuid, menu_id, key):
    postURL = None

    # sub menu
    sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key)

    if (sub_menu_key):
        # get menu link
        menu_link = MenuLink.objects.filter(
            menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

        if(menu_link):
            # create menu session
            session = MenuSession()
            session.channel = channel
            session.code = uuid
            session.menu_id = menu_link[0].link_id

            #check for channel
            if(channel == 'whatsapp'):
                session.phone = phone
            elif(channel == 'telegram'):
                session.message_id = phone

            #save    
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id)

            #check for post data = 1
            menu = Menu.objects.get(pk=menu_link[0].link_id)

            if menu.post_url is not None:
                postURL = menu.post_url
            
        else:
            # message
            message = "Invalid input"
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            # create menu session
            session = MenuSession()
            session.channel = channel
            session.code = uuid
            session.menu_id = menu_link[0].link_id
            #check for channel
            if(channel == 'whatsapp'):
                session.phone = phone
            elif(channel == 'telegram'):
                session.message_id = phone
            #save    
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id)

            #check for post data = 1
            menu = Menu.objects.get(pk=menu_link[0].link_id)

            if menu.post_url is not None:
                postURL = menu.post_url
        else:
            # message
            message = "Invalid input"

    return JsonResponse({'status': 'success', 'message': message, 'postURL': postURL})


# process data
def process_data(uuid):
    menu_sessions = MenuSession.objects.filter(code=uuid)

    if(menu_sessions):
        arr_data = {}
        for menu_session in menu_sessions:
            menu = Menu.objects.get(pk=menu_session.menu_id)
            sub_menu = SubMenu.objects.filter(menu_id=menu.id)

            menu_value = ''
            if(sub_menu):
                sub_menu_value = SubMenu.objects.filter(menu_id=menu.id, view_id=menu_session.values)

                if(sub_menu_value):
                    menu_value = sub_menu_value[0].title

            else:
                menu_value = menu_session.values

            # assign all data to array
            if menu.label is not None and menu_value is not None:
                arr_data[menu.label] = menu_value

        #decide contact based on channel
        contact = ''
        if menu_sessions[0].channel == 'whatsapp':
            contact = menu_sessions[0].phone
        elif  menu_sessions[0].channel == 'telegram':
            contact = menu_sessions[0].message_id
        #response
        response = {
            'contents': arr_data, 
            'channel': menu_sessions[0].channel.upper(), 
            'contact': contact
        }
        return response
    else:
        return []


 #sending data
def send_data(uuid, postURL):
    #process data
    payload = process_data(uuid)

    #post data
    response = requests.post(f"{postURL}/ems/api/signal/", data = json.dumps(payload), headers={"Content-Type": "application/json; charset=utf-8"})
    print(response.json())

    #update sent = 1
    MenuSession.objects.filter(code = uuid).update(sent=1)
        
    #browser response
    return JsonResponse({'status': 'success', 'message': "data sent"})