from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Booking,Current_Booking,Request,Chat
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import BookingForm,ChatForm
from datetime import date, timedelta
import datetime
import time
from threading import Timer
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    else:
        isactive()
        user = request.user
        bookings = Booking.objects.filter(~Q(user=user) & Q(is_active=True))
        requests = Request.objects.filter(from_user=request.user)
        to_bookings = []
        for r in requests:
            to_bookings.append(r.to_booking)
        context = {
        'user':user,
        'bookings':bookings,
        'requests':requests,
        'to_bookings':to_bookings
        }
        return render(request,'cabshare/index.html',context)

def details(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    else:
        isactive()
        bookings = Booking.objects.filter(user = request.user)
        b = bookings.filter(is_active=True)
        requests=Request.objects.none()
        for booking in b:
            requests = requests | Request.objects.filter(to_booking=booking)
        context = {
        'bookings':bookings,
        'requests':requests
        }
        return render(request,'cabshare/details.html',context)
# -------------------------------------------------------------------------------------------------------------------

def BookingCreate(request):
    if request.method=='POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking=form.save(commit=False)
            booking.user=request.user
            booking.is_active = True
            booking.save()
            return redirect('cabshare:current_bookings')
        else:
            return render(request,'cabshare/booking_form.html',{'form':form})
    else:
        form = BookingForm(None)
        return render(request,'cabshare/booking_form.html',{'form':form})


# class BookingCreate(LoginRequiredMixin, CreateView):
#     model = Booking
#     fields = ['date_of_journey','time','destination','amount_of_luggage','budget','special_note']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.is_active = True
#         return super(BookingCreate, self).form_valid(form)

def current_bookings(request):
    booking = Booking.objects.filter(user = request.user)
    cb = booking.order_by('-pk')[0]
    current_booking = Current_Booking(booking=cb)
    current_booking.save()
    pk = current_booking.pk
    return redirect('cabshare:results',pk)
# -------------------------------------------------------------------------------------------------------------------

def isactive():
    for b in Current_Booking.objects.all():
        if b.booking.date_of_journey > date.today():
            continue
        elif b.booking.date_of_journey == date.today():
            if b.booking.time < datetime.datetime.now().time():
                b.booking.is_active = False
                b.booking.save()
                b.delete()
            else:
                continue
        else:
            b.booking.is_active = False
            b.booking.save()
            b.delete()
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

def DeletePrevious(request):
    bookings = Booking.objects.filter(user=request.user,is_active=False)
    for booking in bookings:
        booking.delete()
    return redirect('cabshare:my_bookings')
# ------------------------------------------------------------------------------------------------------------------

def search(request):
    isactive()
    destinationquery = request.GET.get('destination')
    d = request.GET.get('date')
    # time = request.GET.get('time')
    #
    # from_date = time - datetime.timedelta(hours = 2)
    # to_date = time + datetime.timedelta(hours = 2)
    bookings = Booking.objects.filter(is_active=True)
    if destinationquery and date:
        # result = bookings.filter(booking.destination=destinationquery & booking.date=date)
        result = bookings.filter(Q(destination__icontains=destinationquery) & Q(date_of_journey__icontains=d) & ~Q(user=request.user))

        requests = Request.objects.filter(from_user=request.user)
        to_bookings = []
        for r in requests:
            to_bookings.append(r.to_booking)
        context = {
        'result':result,
        'requests':requests,
        'to_bookings':to_bookings
        }

        return render(request,'cabshare/search.html',context)
    else:
        return render(request,'cabshare/error.html')

def results(request,pk):
    isactive()
    query = Current_Booking.objects.get(pk=pk)
    destinationquery = query.booking.destination
    d = query.booking.date_of_journey
    bookings = Booking.objects.filter(is_active=True)
    if destinationquery and date:
        result = bookings.filter(Q(destination__icontains=destinationquery) & Q(date_of_journey__icontains=d) & ~Q(user=request.user))

        requests = Request.objects.filter(from_user=request.user)
        to_bookings = []
        for r in requests:
            to_bookings.append(r.to_booking)
        context = {
        'result':result,
        'requests':requests,
        'to_bookings':to_bookings
        }

        return render(request,'cabshare/search.html',context)
    else:
        return render(request,'cabshare/error.html')
# ---------------------------------------------------------------------------------------------------------------------
def joinrequest(request,pk):
    to_booking = Booking.objects.get(pk=pk)
    from_user = request.user

    request = Request(from_user=from_user,to_booking=to_booking)
    request.save()
    return redirect('cabshare:myrequests')

def cancelrequest(request,pk):
    r = Request.objects.get(pk=pk)
    r.delete()
    return redirect('cabshare:myrequests')

def myrequests(request):
    user = request.user
    requests = Request.objects.filter(from_user=user)
    bookings = []
    for r in requests:
        bookings.append(r.to_booking)
    re=Request.objects.all()
    context = {
        'user':user,
        'bookings':bookings,
        'requests':requests,
        're':re
    }
    return render(request,'cabshare/myrequests.html',context)
# ----------------------------------------------------------------------------------------------------------------------
def viewrequests(request,pk):
    to_booking = Booking.objects.get(pk=pk)
    r = Request.objects.filter(to_booking=to_booking)

    return render(request,'cabshare/viewrequests.html',{'requests':r})

def acceptrequest(request,pk):
    re = Request.objects.get(pk=pk)
    re.accept = True
    re.save()
    to_booking = re.to_booking
    r = Request.objects.filter(to_booking=to_booking)
    return render(request,'cabshare/viewrequests.html',{'requests':r})

def ignorerequest(request,pk):
    re = Request.objects.get(pk=pk)
    to_booking = re.to_booking
    re.delete()
    r = Request.objects.filter(to_booking=to_booking)
    return render(request,'cabshare/viewrequests.html',{'requests':r})
# ----------------------------------------------------------------------------------------------------------------------

def chat(request,pk):
    from_user = request.user
    to_user = User.objects.get(pk=pk)
    chat = Chat.objects.filter(from_user=from_user,to_user=to_user) | Chat.objects.filter(from_user=to_user,to_user=from_user)

    chat = chat.order_by('pk')
    return render(request,'cabshare/chat.html',{'chat':chat,'to_user':to_user,'user':from_user})

def messagesave(request,pk):
    form = ChatForm(None)

    message = request.GET.get('message')
    to_user = User.objects.get(pk=pk)
    new_message = form.save(commit=False)
    new_message.from_user=request.user
    new_message.to_user=to_user
    new_message.message = message
    new_message.save()
    return redirect('cabshare:chat',pk)
# -------------------------------------------------------------------------------------------------------------------------
