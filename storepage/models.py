from django.db import models
from django.apps import apps

class Toko(models.Model):
    nama = models.CharField(max_length=200)
    hari_buka = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    gmaps_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Toko"

    def get_products(self):
        return self.products.all()