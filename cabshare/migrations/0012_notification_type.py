# Generated by Django 3.0.1 on 2020-04-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabshare', '0011_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(default='request', max_length=10),
        ),
    ]