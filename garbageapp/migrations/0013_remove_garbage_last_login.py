# Generated by Django 4.2.14 on 2024-08-20 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garbageapp', '0012_garbage_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garbage',
            name='last_login',
        ),
    ]
