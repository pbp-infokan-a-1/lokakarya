# Generated by Django 5.1 on 2024-10-26 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0005_toko_alter_product_image_product_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ManyToManyField(related_name='store', to='productpage.toko'),
        ),
    ]
