# Generated by Django 5.1.3 on 2024-12-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_author_profile_photo_book_book_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='availability_status',
        ),
        migrations.AddField(
            model_name='book',
            name='available_copies',
            field=models.IntegerField(default=0),
        ),
    ]
