# Generated by Django 3.0.1 on 2020-04-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabshare', '0013_notification_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]