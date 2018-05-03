"""djreact URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views import generic
from django.urls import re_path, path, include
from django.views.generic import TemplateView

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), #To use the auth app we need to add it to our project-level urls.py file.The auth app we’ve now included provides us with several authentication views
    path('toolgate_maps/',include('map.urls')),
]