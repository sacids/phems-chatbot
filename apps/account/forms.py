from django.forms.widgets import Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# User registration
class RegistrationForm(UserCreationForm):
    """
    A class to create user.
    """
    first_name   = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write first name...'}))
    last_name    = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write surname...'}))
    username     = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write username...'}))
    email        = forms.EmailField(max_length=50, required=True, label=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write email...'}))
    password1    = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))
    password2    = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password...'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', )

#user login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label=False, widget=forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-3 text-sm font-normal text-gray-900 placeholder-gray-500 bg-white bg-clip-padding border border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', 'placeholder': 'Write username...'}))
    password = forms.CharField(max_length=20, required=True, label=False, widget=forms.PasswordInput(attrs={'class': 'form-control block w-full px-3 py-3 text-sm font-normal text-gray-900 placeholder-gray-500 bg-white bg-clip-padding border border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', 'placeholder': 'Password...'}))

    class Meta: 
        fields = ('username', 'password')