# Generated by Django 5.1 on 2024-10-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0013_alter_product_category_alter_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
    ]
