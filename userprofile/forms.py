from django import forms
from .models import Profile, Status
from .models import Profile, Status
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'private']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['title', 'description']
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['title', 'description']