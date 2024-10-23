from django.urls import path, include
from django.contrib import admin
from landingpage.views import home

app_name = 'landingpage'

urlpatterns = [
    path('', home, name='home'),
]
