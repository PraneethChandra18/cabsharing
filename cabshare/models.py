from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    date_of_journey = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.",default=None)
    time = models.TimeField(help_text="Please use the following format: <em>HH:MM:SS</em>.",default=None)
    destination = models.CharField(max_length=500)
    amount_of_luggage = models.CharField(max_length=500)
    budget = models.CharField(max_length=100)
    special_note = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True) #Goes inactive after completion of time, helps in searches

    def get_absolute_url(self):
        return reverse('cabshare:current_bookings')

    def __str__(self):
        return self.destination

class Current_Booking(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)

class Request(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    to_booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)

class Chat(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='from_user')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='to_user')
    message = models.TextField()
    seen = models.BooleanField(default=False)

class Notification(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    type = models.CharField(max_length=10,default="request")
    notification = models.TextField()
    seen = models.BooleanField(default=False)
