# Generated by Django 5.1.2 on 2024-10-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0010_alter_product_image'),
        ('storepage', '0006_alter_toko_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ManyToManyField(default=None, related_name='products', to='storepage.toko'),
        ),
    ]