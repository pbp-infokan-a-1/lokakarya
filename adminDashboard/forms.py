from django import forms
from .models import Product, Store, Category, Rating

class ProductForm(forms.ModelForm):
    stores = forms.ModelMultipleChoiceField(
        queryset=Store.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'rating', 'num_reviews', 'stores']

class StoreForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Store
        fields = ['name', 'openDays', 'address', 'email', 'phone', 'products']
