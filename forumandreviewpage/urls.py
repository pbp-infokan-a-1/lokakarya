from django.urls import path
from forumandreviewpage.views import show_forum, create_forum_entry, show_xml, show_json, show_json_by_id, show_xml_by_id
from forumandreviewpage import views

app_name = 'forumandreviewpage'

urlpatterns = [
    path('forumandreviewpage/', views.show_forum, name='show_forum'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_forum_entry, name='create_forum_entry'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]