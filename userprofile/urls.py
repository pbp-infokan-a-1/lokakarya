from django.urls import path
from .views import profile, update_profile
from django.conf import settings
from django.conf.urls.static import static

app_name = 'userprofile'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),  # This is the missing pattern
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)