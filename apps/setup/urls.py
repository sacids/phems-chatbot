from django.urls import path
from . import api

app_name = 'setup'

urlpatterns = [
    path('wards/', api.get_wards , name='wards'),
    path('villages/', api.get_villages , name='villages'),
   
]