# Generated by Django 5.1.3 on 2024-12-11 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_subscription_max_rentals_alter_subscription_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='library/profile_photos/'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, null=True, upload_to='library/images/'),
        ),
    ]
