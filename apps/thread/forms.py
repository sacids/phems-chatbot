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
            'title': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'title', 'placeholder': 'Write title...', 'rows': 3 }),
            'step': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'flag', 'placeholder': 'Write step...', 'required': '' }),
            'flag': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'flag', 'placeholder': 'Write flag...', 'required': '' }),
            'label': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'label', 'placeholder': 'Write label...', 'required': '' }),
            'pull_url': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'url', 'placeholder': 'Write pull url...', }),
            'verify': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'verify', 'placeholder': 'Validate...' }),
            'verify_url': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'verify_url', 'placeholder': 'Write validation url...', }),
            'action': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'action', 'placeholder': 'action...' }),
            'action_url': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'action', 'placeholder': 'Write action url...', }),
        } 

        labels = {
            'title': 'Title',
            'step': 'Step',
            'flag': 'Flag',
            'label': 'Label',
            'pull_url': 'Pull URL',
            'verify': 'Validation',
            'verify_url': 'Validation URL',
            'action': 'Action',
            'action_url': 'Action URL',
        }      
