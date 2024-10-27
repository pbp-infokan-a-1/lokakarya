from django.urls import path
from productpage import views

app_name = 'productpage'
urlpatterns = [
    path('products/', views.product_page, name='product_page'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('favorites/', views.favorite_page, name='favorite_page'),
    path('products/json/', views.show_json, name='show_json'),
    path('products/json/<uuid:product_id>/', views.show_json_by_id, name='show_json_by_id'),
    # Non-API AJAX endpoints
    path('products/<uuid:product_id>/rate/', views.add_review_ajax, name='add_review_ajax'),
    path('products/create/', views.create_product_ajax, name='create_product_ajax'),
    path('products/<uuid:product_id>/update_rate/', views.update_product_ajax, name='update_product_ajax'),
    path('products/<uuid:product_id>/delete_rate/', views.delete_product_ajax, name='delete_product_ajax'),

    # API endpoints
    path('api/products/create/', views.create_product_ajax, name='api_create_product'),
    path('api/products/<uuid:product_id>/rate/', views.add_review_ajax, name='api_add_review'),
    path('api/products/<uuid:product_id>/update/', views.update_product_ajax, name='api_update_product'),
    path('api/products/<uuid:product_id>/delete/', views.delete_product_ajax, name='api_delete_product'),
]