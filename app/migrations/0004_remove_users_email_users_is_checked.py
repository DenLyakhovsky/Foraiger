# Generated by Django 5.0.1 on 2024-01-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_users_name_users_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
        migrations.AddField(
            model_name='users',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='is_checked'),
        ),
    ]
