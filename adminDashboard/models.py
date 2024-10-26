import uuid
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, default='General')

    def __str__(self):
        return self.name

class Rating(models.Model):
    rating_value = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.rating_value)

class Store(models.Model):
    name = models.CharField(max_length=200, default='Unnamed Store')
    openDays = models.CharField(max_length=100, default='Monday to Friday')
    address = models.TextField(default='No address available.')
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=20, default='000-000-0000')
    products = models.ManyToManyField('Product', related_name='stores')  # Many-to-Many field in Store

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='Unnamed Product')
    image = models.ImageField(upload_to='product_images/', default='default.jpg')
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField(default='No description available.')
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True)
    num_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.name
