from django.urls import path
from .views import profile, update_profile_ajax, update_status_ajax, delete_status, edit_status, status_json, status_json_by_id

app_name = 'userprofile'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/update/ajax', update_profile_ajax, name='update_profile_ajax'),  # This is the missing pattern
    path('edit-status/<int:status_id>', edit_status, name='edit_status'),
    path('delete/<int:status_id>', delete_status, name='delete_status'),
    path('profile/updatestatus/ajax', update_status_ajax, name='update_status_ajax'),
    path('json/', status_json, name='status_json'),
    path('json/<str:status_id>/', status_json_by_id, name='status_json_by_id'),
]