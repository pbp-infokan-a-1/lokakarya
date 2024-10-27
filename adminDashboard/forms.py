from django import forms
from storepage.models import Toko
from productpage.models import Category, Product

class TokoForm(forms.ModelForm):
    class Meta:
        model = Toko
        fields = ['nama', 'hari_buka', 'alamat', 'email', 'telepon', 'image', 'gmaps_link']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Store Name'}),
            'hari_buka': forms.TextInput(attrs={'placeholder': 'Open Days'}),
            'alamat': forms.Textarea(attrs={'placeholder': 'Store Address'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Store Email'}),
            'telepon': forms.TextInput(attrs={'placeholder': 'Store Phone'}),
            'gmaps_link': forms.URLInput(attrs={'placeholder': 'Google Maps Link'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category Name'}),
        }

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'placeholder': 'Select Category'}))

    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'store', 'min_price', 'max_price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'store': forms.SelectMultiple(attrs={'placeholder': 'Select Stores'}),
            'min_price': forms.NumberInput(attrs={'placeholder': 'Minimum Price'}),
            'max_price': forms.NumberInput(attrs={'placeholder': 'Maximum Price'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description'}),
        }