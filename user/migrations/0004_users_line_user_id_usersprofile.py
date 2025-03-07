# Generated by Django 4.2.16 on 2024-11-06 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_users_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='line_user_id',
            field=models.TextField(default='', max_length=512),
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(max_length=512, unique=True)),
                ('name', models.TextField(max_length=512)),
                ('profile_picture_url', models.TextField(blank=True, default='', max_length=5000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.users')),
            ],
        ),
    ]
