# Generated by Django 4.2.4 on 2023-08-24 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='profile_images/'),
        ),
    ]
