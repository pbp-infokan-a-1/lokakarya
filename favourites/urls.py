from . import views
from django.urls import path

urlpatterns = [
    path('toggle/<str:product_id>/', views.toggle_favorite, name='toggle'),
    path('view/', views.view_all_favorites_by_user, name='view_all_favorites'),
    path('view/<str:user_id>/', views.view_all_favorites_by_user_id, name='view_all_favorites_by_user_id'),
    path('test', views.test, name="test")
]
