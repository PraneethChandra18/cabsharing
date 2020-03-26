from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class login_model(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=100)


class Gender(models.Model):
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.gender


class User_profile(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=100)
    photo = models.FileField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    hostel = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    bio = models.TextField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse('account:profile-view')

    def __str__(self):
        return self.bio
