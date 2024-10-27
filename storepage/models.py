from django.db import models
# from productpage.models import Product

class Toko(models.Model):
    nama = models.CharField(max_length=200)
    hari_buka = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    image = models.CharField(max_length=255, blank=True)
    gmaps_link = models.URLField(blank=True, null=True)
    page_link = models.URLField(blank=True, null=True)
    # produk = models.ManyToManyField(Product, related_name='toko')

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Toko"