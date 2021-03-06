# Generated by Django 3.0.1 on 2020-03-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabshare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_of_journey',
            field=models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.TimeField(help_text='Please use the following format: <em>HH-MM-SS</em>.'),
        ),
    ]
