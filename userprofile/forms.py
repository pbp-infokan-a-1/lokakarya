from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

def validate_image_file_extension(file):
    ext = file.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('Only image files with .jpg, .jpeg, .png extensions are allowed.')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

