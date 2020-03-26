from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    date_of_journey = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    time = models.TimeField(help_text="Please use the following format: <em>HH-MM-SS</em>.")
    destination = models.CharField(max_length=500)
    amount_of_luggage = models.CharField(max_length=500)
    budget = models.CharField(max_length=100)
    special_note = models.TextField()
    is_active = models.BooleanField(default=True) #Goes inactive after completion of time, helps in searches

    def get_absolute_url(self):
        return reverse('cabshare:current_bookings')

    def __str__(self):
        return self.destination
