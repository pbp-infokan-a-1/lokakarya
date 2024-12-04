from django.urls import path
from auth.views import login, register_app

app_name = 'auth'

path('login_app/', login, name='login_app'),
path('register_app/', register_app, name='register_app'),