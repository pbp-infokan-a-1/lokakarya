from django.urls import path
from landingpage.views import home

app_name = 'landingpage'

urlpatterns = [
    path('', home, name='home'),
]
