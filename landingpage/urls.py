from django.urls import path, include
from django.contrib import admin
from landingpage.views import home, search, search_mobile

app_name = 'landingpage'

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('search_mobile/', search_mobile, name='search_mobile'),
]
