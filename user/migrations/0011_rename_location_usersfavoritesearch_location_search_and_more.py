# Generated by Django 4.2.16 on 2024-11-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_users_tier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersfavoritesearch',
            old_name='location',
            new_name='location_search',
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
