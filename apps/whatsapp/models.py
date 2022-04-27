import random
import string
from django.db import models
from django.http import JsonResponse

# Create your models here.
class Menu(models.Model):
    title       =  models.TextField(blank=False, null=False)
    flag        =  models.CharField(max_length=50, blank=False, null=False)
    label       =  models.CharField(max_length=50, blank=True, null=True)
    verify      =  models.IntegerField(default=0, null=False)
    url         =  models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'cb_menus'
        verbose_name_plural = 'Menu'

    def __str__(self):
        return self.title


class SubMenu(models.Model):
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE)
    view_id     =  models.CharField(max_length=10, blank=False, null=False)
    title       =  models.TextField(blank=False, null=False)
    

    class Meta:
        db_table = 'cb_sub_menus'
        verbose_name_plural = 'Sub Menus'

    def __str__(self):
        return self.title    


class MenuLink(models.Model):
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    sub_menu    =  models.ForeignKey(SubMenu, on_delete=models.DO_NOTHING, blank=True, null=True)
    link        =  models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='link')

    class Meta:
        db_table = 'cb_menu_links'
        verbose_name_plural = 'Menu Links' 


class MenuSession(models.Model):
    code        =  models.CharField(max_length=100, blank=True, null=True)
    phone       =  models.CharField(max_length=100, blank=True, null=True)
    message_id  =  models.CharField(max_length=100, blank=True, null=True)
    channel     =  models.CharField(max_length=100, blank=False, null=False, default='whatsapp')  
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE)
    values      =  models.TextField(blank=True, null=True)
    active      =  models.IntegerField(blank=False, null=False, default=0)
    sent        =  models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'cb_menu_sessions'
        verbose_name_plural = 'Menu Sessions' 

#init menu
def init_menu(channel, phone):
    # get first menu
    menu = Menu.objects.get(flag='Menu_Tukio')

    #generate random key
    random_code = ''.join(random.choices(string.ascii_uppercase, k=12))

    # create menu session
    session = MenuSession()
    session.channel = channel
    session.phone = phone
    session.code = random_code
    session.menu_id = menu.id
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
            return True
        else:
            return False
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            return True
        else:
            return False

#next menu
def next_menu(channel, phone, uuid, menu_id, key):
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
            session.phone = phone
            session.code = uuid
            session.menu_id = menu_link[0].link_id
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id)
        else:
            # message
            message = "Invalid input"
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            # create menu session
            session = MenuSession()
            session.channel = channel
            session.phone = phone
            session.code = uuid
            session.menu_id = menu_link[0].link_id
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id)
        else:
            # message
            message = "Invalid input"

    return JsonResponse({'status': 'success', 'message': message})


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
                sub_menu_value = SubMenu.objects.filter(menu_id=menu.id, sequence=menu_session.values)

                if(sub_menu_value):
                    menu_value = sub_menu_value[0].title

            else:
                menu_value = menu_session.values

            # assign all data to array
            arr_data[menu.label] = menu_value
        #response
        response = {"channel": "ChatBot", "contents": arr_data}
        return response
    else:
        return []