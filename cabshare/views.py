from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import date, datetime
import time
from threading import Timer
CURRENT_BOOKINGS = [];

def index(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    else:
        user = request.user
        context = {
        'user':user
        }
        return render(request,'cabshare/index.html',context)

def details(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    else:
        bookings = Booking.objects.filter(user = request.user)
        context = {
        'bookings':bookings
        }
        return render(request,'cabshare/details.html',context)
# -------------------------------------------------------------------------------------------------------------------
class BookingCreate(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['date_of_journey','time','destination','amount_of_luggage','budget','special_note']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_active = True
        return super(BookingCreate, self).form_valid(form)

def current_bookings(request):
    booking = Booking.objects.filter(user = request.user)
    cb = booking.order_by('-pk')[0]
    CURRENT_BOOKINGS.append(cb)
    print(CURRENT_BOOKINGS)
    return redirect('cabshare:my_bookings')
# -------------------------------------------------------------------------------------------------------------------

# not working properly
def isactive(request):
    for booking in CURRENT_BOOKINGS:
        if booking.date_of_journey > date.today():
            continue
        elif booking.date_of_journey == date.today():
            if booking.time < datetime.now().time():
                booking.is_active = False
                CURRENT_BOOKINGS.remove(booking)
            else:
                continue
        else:
            booking.is_active = False
            CURRENT_BOOKINGS.remove(booking)

    print(CURRENT_BOOKINGS)
    # Timer(10, isactive(request)).start()
    return redirect('cabshare:my_bookings')
# -------------------------------------------------------------------------------------------------------------------
class BookingUpdate(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['date_of_journey','time','destination','amount_of_luggage','budget','special_note']

class BookingDelete(DeleteView):
    model=Booking
    success_url=reverse_lazy('cabshare:my_bookings')

    def get(self, *args, **kwargs):
            return self.post(*args, **kwargs)
