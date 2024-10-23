import uuid
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    category = models.ManyToManyField(Category)
    # store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    num_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

