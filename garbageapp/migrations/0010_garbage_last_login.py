# Generated by Django 4.2.14 on 2024-08-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garbageapp', '0009_booking_selected_plant'),
    ]

    operations = [
        migrations.AddField(
            model_name='garbage',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
