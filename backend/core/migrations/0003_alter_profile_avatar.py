# Generated by Django 5.2 on 2025-04-24 03:18

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_avatar_url_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='Image'),
            preserve_default=False,
        ),
    ]
