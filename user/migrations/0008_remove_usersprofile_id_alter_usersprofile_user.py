# Generated by Django 4.2.16 on 2024-11-11 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_room_usersfavoritesearch_room_from_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.users'),
        ),
    ]
