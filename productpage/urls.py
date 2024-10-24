from django.urls import path
from productpage import views

app_name = 'productpage'
urlpatterns = [
    path('products/', views.product_page, name='product_page'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('favorites/', views.favorite_page, name='favorite_page'),
]

