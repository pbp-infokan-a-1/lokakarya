# Generated by Django 5.1 on 2024-10-26 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboard', '0005_alter_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='store',
            name='products',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
    ]
