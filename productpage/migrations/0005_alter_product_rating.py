# Generated by Django 5.1.1 on 2024-10-25 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='productpage.rating'),
        ),
    ]
