import uuid
from django.db import models
from django.contrib.auth.models import User
from storepage.models import Toko

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

class Toko(models.Model):
    nama = models.CharField(max_length=200)
    hari_buka = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    # produk = models.ManyToManyField(Product, related_name='toko')

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    category = models.ManyToManyField(Category)
    store = models.ManyToManyField(Toko, related_name='products')
    price = models.CharField(max_length=20)
    description = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True)
    num_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
