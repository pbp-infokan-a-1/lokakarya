from django.forms import ModelForm
from forumandreviewpage.models import PostForum, Comment


class ForumandReviewForm(ModelForm):
    class Meta:
        model = PostForum
        fields = ["title", "content"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]