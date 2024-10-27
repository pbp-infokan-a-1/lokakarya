from django import forms
from .models import Toko

class StoreForm(forms.ModelForm):
    class Meta:
        model = Toko
        fields = ['nama', 'alamat', 'hari_buka', 'email', 'telepon', 'image']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-input'}),
            'alamat': forms.Textarea(attrs={'class': 'form-input'}),
            'hari_buka': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telepon': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.match(r'^[\w\.-]+@[\w\.-]+\.\w+$'):
            raise forms.ValidationError("Invalid email format")
        return email
