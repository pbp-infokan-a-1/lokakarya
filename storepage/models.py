from django.db import models

class Toko(models.Model):
    nama = models.CharField(max_length=200)
    hari_buka = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Toko"