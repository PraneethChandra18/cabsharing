# Generated by Django 3.0.1 on 2020-05-03 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabshare', '0015_auto_20200503_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='destination',
            field=models.CharField(choices=[('IIT GUWAHATI', 'IIT GUWAHATI'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')], default='IIT GUWAHTI', max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='starting_point',
            field=models.CharField(choices=[('IIT GUWAHATI', 'IIT GUWAHATI'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')], default='IIT GUWAHATI', max_length=100),
        ),
    ]
