import uuid
from django.db import models
from django.contrib.auth.models import User
# from storepage.models import Store

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='ratings', on_delete=models.CASCADE, default=None)
    rating = models.FloatField(default=0)
    review = models.TextField(blank=True, null=True)  # Optional review text

    def __str__(self):
        return f'Rating: {self.rating} by {self.user.username}'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=None)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()

    def average_rating(self):
        avg_rating = self.ratings.aggregate(models.Avg('rating'))['rating__avg']
        return avg_rating or 0  # Return 0 if no ratings

    def num_reviews(self):
        return self.ratings.count()

    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
