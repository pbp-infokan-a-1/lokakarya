# admin.py
from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'num_reviews')
    filter_horizontal = ('category',)  #easy selection of multiple categories

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
