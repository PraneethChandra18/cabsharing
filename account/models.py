from django.db import models

# Create your models here.

class login_model(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=100)
