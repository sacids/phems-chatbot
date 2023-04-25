"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.whatsapp import views as whatsapp_views
from apps.telegram import views as telegram_views
from apps.api import views as api_views
from apps.thread.validation import *

urlpatterns = [
    path('', include('apps.account.urls')),
    path('accounts/', include('apps.account.urls')),
    path('admin/', admin.site.urls),
    path('setup/', include('apps.setup.urls')),
    path('threads/', include('apps.thread.urls')),

    path('webhook/testing', whatsapp_views.testing),
    path('webhook/facebook', whatsapp_views.facebook),
    path('webhook/telegram', telegram_views.index),
    path('privacy_policy', whatsapp_views.privacy_policy),

    path('api/validation/village', validate_village),
    path('api/validation/ward', validate_ward),
    path('api/validation/date', validate_date),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
