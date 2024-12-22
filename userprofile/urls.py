from django.urls import path
from .views import profile, update_profile_ajax, update_status_ajax, status_json, edit_status, delete_status, create_status_flutter, show_json_profile, update_profile_app, get_profile

app_name = 'userprofile'

urlpatterns = [
    path('show-json/', show_json_profile, name='show_json_profile'),
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/update/ajax', update_profile_ajax, name='update_profile_ajax'),
    path('profile/<str:username>/update_app/', update_profile_app, name='update_profile_app'),
    path('profile/<str:username>/status/', status_json, name='status_json'),
    path('edit-status/<int:status_id>', edit_status, name='edit_status'),
    path('delete/<int:status_id>', delete_status, name='delete_status'),
    path('profile/<str:username>/status/update/ajax', update_status_ajax, name='update_status_ajax'),
    path('create-flutter/', create_status_flutter, name='create_status_flutter'),
    path('profile/<str:username>/get/', get_profile, name='get_profile'),
]
