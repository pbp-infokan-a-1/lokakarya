from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'storepage' 

urlpatterns = [
    path('toko/', views.toko_list, name='storepage'),
    path('store/create/', views.create_store, name='create_store'),
    path('store/update/<int:store_id>/', views.update_store, name='update_store'),
    path('store/delete/<int:store_id>/', views.delete_store, name='delete_store'),
    path('api/store/create/', views.create_store, name='create_store'),
    path('api/store/update/<int:store_id>/', views.update_store, name='update_store'),
    path('api/store/delete/<int:store_id>/', views.delete_store, name='delete_store'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)