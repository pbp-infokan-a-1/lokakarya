from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'storepage' 

urlpatterns = [
    path('toko/', views.toko_list, name='storepage'),
    path('toko/<int:store_id>/', views.storedetail, name='storedetail'),
    path('api/store/create/', views.store_api_create, name='store_api_create'),
    path('api/store/update/<int:pk>/', views.store_api_update, name='store_api_update'),
    path('api/store/delete/<int:pk>/', views.store_api_delete, name='store_api_delete'),
    path('api/store/<int:pk>/', views.store_api_get, name='store_api_get'),
    path('toko/show_all/', views.show_all_json, name='show_all_json'),
    path('toko/fetch-image/<int:store_id>/', views.fetch_image, name='fetch_image'),
    path('toko/<int:store_id>/products/json/', views.store_products_json, name='store_products_json'),
    path('toko/products/<uuid:product_id>/image/', views.fetch_product_image, name='fetch_product_image'),
    path('toko/api/create/', views.add_store_flutter, name='add_store_flutter'),
    path('toko/api/<int:store_id>/edit/', views.edit_store_flutter, name='edit_store_flutter'),
    path('toko/api/<int:store_id>/delete/', views.delete_store_flutter, name='delete_store_flutter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)