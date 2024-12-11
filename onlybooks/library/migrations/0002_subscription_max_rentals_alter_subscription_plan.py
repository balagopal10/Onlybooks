# Generated by Django 5.1.3 on 2024-12-10 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='max_rentals',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Platinum', 'Platinum'), ('Diamond', 'Diamond')], max_length=50),
        ),
    ]