# Generated by Django 4.2.16 on 2024-10-16 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_users_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='salt',
            field=models.TextField(default='', max_length=512),
        ),
    ]