# Generated by Django 3.0.1 on 2020-03-08 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
