from django.urls import path
from . import views
from reviewpage.views import review_list, create_review, delete_review, edit_review, helpful_review, unhelpful_review

app_name = 'reviewpage'

urlpatterns = [
    path('reviewpage/', review_list, name='review_list'),
    path('createreview/', create_review, name='create_review'),
    path('delete_review/<uuid:review_id>/', delete_review, name='delete_review'),
    path('edit_review/<uuid:review_id>/', edit_review, name='edit_review'),
    path('helpful/<uuid:review_id>/', helpful_review, name='helpful_review'),
    path('unhelpful/<uuid:review_id>/', unhelpful_review, name='unhelpful_review'),
]
