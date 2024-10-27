from django.urls import path
from . import views

urlpatterns = [
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<uuid:product_id>/', views.update_product, name='update_product'),  # Use <uuid:product_id>
    path('products/delete/<uuid:product_id>/', views.delete_product, name='delete_product'),  # Use <uuid:product_id>
    path('stores/', views.store_list, name='store_list'),
    path('stores/create/', views.create_store, name='create_store'),
    path('stores/update/<int:store_id>/', views.update_store, name='update_store'),
    path('stores/delete/<int:store_id>/', views.delete_store, name='delete_store'),
]
