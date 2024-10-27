from django import forms
from reviewpage.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={
        'class': 'w-full p-2 border border-gray-300 rounded', 
        'placeholder': 'Rate between 1 and 5'
    }))

    class Meta:
        model = Review
        fields = ["title", "content", "rating"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'rows': 5}),
        }
