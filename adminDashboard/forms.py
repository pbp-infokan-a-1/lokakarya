from django import forms
from .models import Product, Store

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'rating', 'num_reviews', 'store']  # Updated fields

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'openDays', 'address', 'email', 'phone', 'product']  # Updated fields
