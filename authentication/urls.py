from django.urls import path
from authentication.views import register, login_user, logout_user, login_app, register_app, logout_app

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login_app/', login_app, name='login_app'),
    path('register_app/', register_app, name='register_app'),
    path('logout_app/', logout_app, name='logout_app'),
]