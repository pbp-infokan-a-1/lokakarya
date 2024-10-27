from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write your review...', 'rows': 4}),
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }
        labels = {
            'rating': 'Rating',
            'review': 'Review',
        }
