# Generated by Django 5.1 on 2024-10-24 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to='avatars/'),
        ),
    ]
