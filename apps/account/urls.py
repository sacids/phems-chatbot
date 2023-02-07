from django.urls import path
from django.urls.resolvers import URLPattern
from .views import LogoutView, LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", LoginView.as_view() , name="login"),  
    path("login/", LoginView.as_view() , name="login"),  
    path("logout/", LogoutView.as_view(), name="logout"), 
]