# Generated by Django 4.2.16 on 2024-11-30 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_rename_location_usersfavoritesearch_location_search_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersfavoritesearch',
            name='limit',
            field=models.IntegerField(default=5),
        ),
    ]
