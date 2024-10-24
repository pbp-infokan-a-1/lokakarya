import uuid
from django.db import models
from django.contrib.auth.models import User

class PostForum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes', blank=True)

    def total_upvotes(self):
        return self.upvotes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(PostForum, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'