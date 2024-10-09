from django.urls import path
from landingpage.views import home

urlpatterns = [
    path('', home, name='home'),
]
