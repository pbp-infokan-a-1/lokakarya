from django.forms import ModelForm
from forumandreviewpage.models import PostForum, Comment
from django import forms


class ForumandReviewForm(ModelForm):
    class Meta:
        model = PostForum
        fields = ["title", "content"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'rows': 5}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]