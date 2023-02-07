from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import  LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

# Create your views here.
class LoginView(View):
    """Login class"""
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('threads:lists')

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                remember_me = request.POST.get("remember_me")
                if remember_me is True:
                    ONE_MONTH = 30 * 24 * 60 * 60
                    expiry = getattr(
                        settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                    request.session.set_expiry(expiry)

                # redirect
                return redirect(self.success_url)
            else:
                messages.error(request, 'Wrong credentials, try again!')

       # render
        return render(request, self.template_name, {'form': form})

        
class LogoutView(View):
    """Logout fxn"""
    def get(self, request):
        logout(request)
        messages.error(request, 'Log out successfully')
        return redirect('login')
