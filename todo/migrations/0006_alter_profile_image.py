# Generated by Django 4.2.7 on 2023-12-05 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
