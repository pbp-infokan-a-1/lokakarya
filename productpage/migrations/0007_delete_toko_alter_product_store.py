# Generated by Django 5.1 on 2024-10-26 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0006_alter_product_store'),
        ('storepage', '0002_toko_delete_store'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Toko',
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ManyToManyField(related_name='store', to='storepage.toko'),
        ),
    ]