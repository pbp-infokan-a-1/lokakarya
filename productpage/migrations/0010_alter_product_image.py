# Generated by Django 5.1.2 on 2024-10-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0009_rating_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='/avatars/defaults.jpeg', upload_to='media/'),
        ),
    ]
