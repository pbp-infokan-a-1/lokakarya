from django.urls import path
from .views import profile, update_profile_ajax, update_status_ajax, status_json, edit_status, delete_status

app_name = 'userprofile'

urlpatterns = [
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/update/ajax', update_profile_ajax, name='update_profile_ajax'),
    path('profile/<str:username>/status', status_json, name='status_json'),
    path('edit-status/<int:status_id>', edit_status, name='edit_status'),
    path('delete/<int:status_id>', delete_status, name='delete_status'),
    path('profile/<str:username>/status/update/ajax', update_status_ajax, name='update_status_ajax'),
]
