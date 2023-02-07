from django.forms.widgets import Textarea
import datetime
from datetime import timedelta
from django import forms
from .models import *

class ThreadForm(forms.ModelForm):
    """
    A class to create form
    """
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['action'].empty_label  = 'Select'

    class Meta:
        model  = Thread
        exclude = ('created_by', 'updated_by', 'relate')
        fields  = ('__all__')

        widgets = {
            'title': forms.Textarea(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'title', 'placeholder': 'Write title...', 'rows': 3 }),
            'step': forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'flag', 'placeholder': 'Write step...', 'required': '' }),
            'flag': forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'flag', 'placeholder': 'Write flag...', 'required': '' }),
            'label': forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'label', 'placeholder': 'Write label...', 'required': '' }),
            'pull': forms.NumberInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'pull', 'placeholder': 'pull...', 'required': '' }),
            'url': forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'url', 'placeholder': 'Write pull url...', }),
            'action': forms.Select(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'action', 'placeholder': 'action...' }),
            'action_url': forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500', 'id': 'action', 'placeholder': 'Write action url...', }),
        } 

        labels = {
            'title': 'Title',
            'step': 'Step',
            'flag': 'Flag',
            'label': 'Label',
            'pull': 'Pull',
            'url': 'Pull URL',
            'action': 'Action',
            'action_url': 'Action URL',
        }      
