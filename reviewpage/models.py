import uuid
from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    helpful = models.ManyToManyField(User, related_name='review_helpful', blank=True)
    total_helpful = models.IntegerField(default=0)
    unhelpful = models.ManyToManyField(User, related_name='review_unhelpful', blank=True)
    total_unhelpful = models.IntegerField(default=0)

    def calculate_total_helpful(self):
        return self.helpful.count()
    
    def calculate_total_unhelpful(self):
        return self.unhelpful.count()

    def __str__(self):
        return f'{self.reviewer_name} - {self.title}'