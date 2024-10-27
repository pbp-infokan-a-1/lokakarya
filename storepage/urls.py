from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import toko_list, create_store, update_store, delete_store, storedetail

app_name = 'storepage' 

urlpatterns = [
    path('toko/', views.toko_list, name='storepage'),
    path('toko/create/', views.create_store, name='create_store'),
    path('toko/update/<int:store_id>/', views.update_store, name='update_store'),
    path('toko/delete/<int:store_id>/', views.delete_store, name='delete_store'),
    path('api/toko/create/', views.create_store, name='create_store'),
    path('api/toko/update/<int:store_id>/', views.update_store, name='update_store'),
    path('api/toko/delete/<int:store_id>/', views.delete_store, name='delete_store'),
    path('toko/<int:store_id>/', storedetail, name='storedetail')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)