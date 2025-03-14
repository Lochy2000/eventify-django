# Generated by Django 5.1.6 on 2025-03-14 11:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='default_profile_ju9xum', max_length=255, verbose_name='avatar'),
        ),
    ]
