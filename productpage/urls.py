from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from productpage import views

app_name = 'productpage'
urlpatterns = [
    path('products/', views.product_page, name='product_page'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('favorites/', views.favorite_page, name='favorite_page'),
    path('products/json/', views.show_json, name='show_json'),
    path('products/json/<uuid:product_id>/', views.show_json_by_id, name='show_json_by_id'),
    path('products/<uuid:product_id>/redirect_to_store/', views.redirect_to_store, name='redirect_to_store'),
    path('products/<str:product_name>/', views.product_detail, name='product_detail_by_name'),

    # Non-API AJAX endpoints
    path('products/<uuid:product_id>/rate/', views.add_review_ajax, name='add_review_ajax'),
    path('products/<uuid:product_id>/update_rate/<int:review_id>/', views.edit_review_ajax, name='edit_review_ajax'),
    path('products/<uuid:product_id>/delete_rate/<int:review_id>/', views.delete_review_ajax, name='delete_review_ajax'),

    # API endpoints
    path('api/products/<uuid:product_id>/rate/', views.add_review_ajax, name='api_add_review'),
    path('api/products/<uuid:product_id>/update_rate/<int:review_id>/', views.edit_review_ajax, name='api_edit_review'),
    path('api/products/<uuid:product_id>/delete_rate/<int:review_id>/', views.delete_review_ajax, name='api_delete_review'),

    # Flutter API
    path('flutterproducts/', views.product_list_view, name='product-list'),
    path('fluttercategories/', views.category_list_view, name='category-list'),
    path('api/products/<uuid:product_id>/', views.product_detail_flutter, name='product_detail_flutter'),
    path('api/products/<uuid:product_id>/reviews/', views.add_review_flutter, name='add_review_flutter'),
    path('api/products/<uuid:product_id>/edit_reviews/<int:review_id>/', views.edit_review_flutter, name='edit_review_flutter'),
    path('api/products/<uuid:product_id>/delete_reviews/<int:review_id>/', views.delete_review_flutter, name='delete_review_flutter'),

    re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
