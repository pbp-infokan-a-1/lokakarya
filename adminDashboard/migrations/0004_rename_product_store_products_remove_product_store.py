# Generated by Django 5.1 on 2024-10-26 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboard', '0003_product_store_alter_store_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='product',
            new_name='products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='store',
        ),
    ]
