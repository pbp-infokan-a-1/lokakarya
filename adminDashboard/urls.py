from django.urls import path
from . import views

urlpatterns = [
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
    path('products/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<str:product_id>/', views.delete_product, name='delete_product'),
    path('stores/', views.store_list, name='store_list'),
    path('add_store/', views.add_store, name='add_store'),
    path('edit_store/<int:store_id>/', views.edit_store, name='edit_store'),
    path('delete_store/<int:store_id>/', views.delete_store, name='delete_store'),
]