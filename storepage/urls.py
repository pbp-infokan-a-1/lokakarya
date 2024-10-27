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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)