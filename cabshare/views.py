from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Booking,Current_Booking,Request,Chat,Notification
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import BookingForm,ChatForm,FeedbackForm
from datetime import date, timedelta
import datetime
import time
from threading import Timer
from django.db.models import Q
import json
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
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

@login_required
def details(request):
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

@login_required
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
    fields = ['date_of_journey','time','starting_point','destination','amount_of_luggage','budget','special_note']

class BookingDelete(LoginRequiredMixin, DeleteView):
    model=Booking
    success_url=reverse_lazy('cabshare:my_bookings')

    def get(self, *args, **kwargs):
            return self.post(*args, **kwargs)

@login_required
def DeletePrevious(request):
    bookings = Booking.objects.filter(user=request.user,is_active=False)
    for booking in bookings:
        booking.delete()
    return redirect('cabshare:my_bookings')
# ------------------------------------------------------------------------------------------------------------------

@login_required
def search(request):
    isactive()
    starting_point = request.GET.get('starting_point')
    destinationquery = request.GET.get('destination')
    d = request.GET.get('date')
    time = request.GET.get('time')
    #
    # from_date = time - datetime.timedelta(hours = 2)
    # to_date = time + datetime.timedelta(hours = 2)

    bookings = Booking.objects.filter(is_active=True)
    result=Booking.objects.none()
    if destinationquery and date and time:
        req = int(time[0:2])
        low = req-2
        high = req+2
        if low<0:
            low=0
        if high>23:
            high=23
        mintime = str(low)
        maxtime = str(high)

        result = bookings.filter(Q(starting_point__icontains=starting_point) & Q(destination__icontains=destinationquery) & Q(date_of_journey__icontains=d) & Q(time__hour__gte=mintime, time__hour__lte=maxtime) & ~Q(user=request.user))
    elif destinationquery and date:
        result = bookings.filter(Q(starting_point__icontains=starting_point) & Q(destination__icontains=destinationquery) & Q(date_of_journey__icontains=d) & ~Q(user=request.user))
    elif destinationquery:
        result = bookings.filter(Q(starting_point__icontains=starting_point) & Q(destination__icontains=destinationquery) & ~Q(user=request.user))
    else:
        return render(request,'cabshare/error.html')

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

def results(request,pk):
    isactive()
    query = Current_Booking.objects.get(pk=pk)
    starting_point = query.booking.starting_point
    destinationquery = query.booking.destination
    d = query.booking.date_of_journey
    time = str(query.booking.time)

    req = int(time[0:2])
    low = req-2
    high = req+2
    if low<0:
        low=0
    if high>23:
        high=23
    mintime = str(low)
    maxtime = str(high)

    bookings = Booking.objects.filter(is_active=True)
    if destinationquery and date and time:
        result = bookings.filter(Q(starting_point__icontains=starting_point) & Q(destination__icontains=destinationquery) & Q(date_of_journey__icontains=d) & Q(time__hour__range=[mintime,maxtime]) & ~Q(user=request.user))

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
@login_required
def joinrequest(request):
    pk = request.GET.get('inputValue')
    to_booking = Booking.objects.get(pk=pk)
    from_user = request.user
    r = Request(from_user=from_user,to_booking=to_booking)
    r.save()
    data = {
        'pk': r.pk
            }
    return JsonResponse(data)

@login_required
def cancelrequest(request):
    pk = request.GET.get('inputValue')
    r = Request.objects.get(pk=pk)
    booking = r.to_booking
    booking_pk = booking.pk
    booking_user_pk = booking.user.pk
    r.delete()
    booking_name = booking.__str__()

    type = request.GET.get('type')

    if type=="untag":
        booking.going_together = booking.going_together - 1
        booking.save()

    data = {
        'booking_pk': booking_pk,
        'booking_user_pk': booking_user_pk,
        'booking_name':booking_name
            }

    return JsonResponse(data)

# def joinrequest(request,pk):
#     to_booking = Booking.objects.get(pk=pk)
#     from_user = request.user
#     r = Request(from_user=from_user,to_booking=to_booking)
#     r.save()
#     return redirect('cabshare:index')
#
# def cancelrequest(request,pk):
#     r = Request.objects.get(pk=pk)
#     r.delete()
#
#     return redirect('cabshare:index')

@login_required
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
@login_required
def viewrequests(request,pk):
    to_booking = Booking.objects.get(pk=pk)
    r = Request.objects.filter(to_booking=to_booking)
    user = request.user
    return render(request,'cabshare/viewrequests.html',{'requests':r,'user':user,'booking':to_booking})

@login_required
def viewrequestsothers(request,pk):
    to_booking = Booking.objects.get(pk=pk)
    r = Request.objects.filter(to_booking=to_booking)
    return render(request,'cabshare/viewrequestsothers.html',{'requests':r,'booking':to_booking})

@login_required
def acceptrequest(request):
    pk = request.GET.get('inputValue')
    re = Request.objects.get(pk=pk)
    re.accept = True
    re.save()
    to_booking = re.to_booking
    to_booking.going_together = to_booking.going_together + 1
    to_booking.save()

    data = {
        'pk': pk
            }

    return JsonResponse(data)

# def acceptrequest(request,pk):
#     re = Request.objects.get(pk=pk)
#     re.accept = True
#     re.save()
#     to_booking = re.to_booking
#     r = Request.objects.filter(to_booking=to_booking)
#
#     return render(request,'cabshare/viewrequests.html',{'requests':r})

@login_required
def ignorerequest(request):
    pk = request.GET.get('inputValue')
    re = Request.objects.get(pk=pk)
    to_booking = re.to_booking
    re.delete()

    type = request.GET.get('type')

    if type=="untag":
        to_booking.going_together = to_booking.going_together - 1
        to_booking.save()

    data = {
        'pk': pk
            }

    return JsonResponse(data)

# ----------------------------------------------------------------------------------------------------------------------

@login_required
def chat(request,pk):
    from_user = request.user
    to_user = User.objects.get(pk=pk)
    chat = Chat.objects.filter(from_user=from_user,to_user=to_user) | Chat.objects.filter(from_user=to_user,to_user=from_user)
    ch = chat.filter(to_user=from_user,seen=False)
    for c in ch:
        c.seen = True
        c.save()

    chat = chat.order_by('pk')
    return render(request,'cabshare/chat.html',{'chat':chat,'to_user':to_user,'user':from_user})

@login_required
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

@login_required
def deletechat(request,pk):
    from_user = request.user
    to_user = User.objects.get(pk=pk)
    chat = Chat.objects.filter(from_user=from_user,to_user=to_user) | Chat.objects.filter(from_user=to_user,to_user=from_user)

    for c in chat:
        c.delete()
    return redirect('cabshare:chat',pk)
# -------------------------------------------------------------------------------------------------------------------------

@login_required
def mychats(request):
    user = request.user
    chat = Chat.objects.filter(from_user=user) | Chat.objects.filter(to_user=user)
    chat = chat.order_by('-pk')
    with_users = []

    for message in chat:
        if message.from_user == user:
            if not message.to_user in with_users:
                with_users.append(message.to_user)
        else:
            if not message.from_user in with_users:
                with_users.append(message.from_user)

    with_users_dict = {}
    for u in with_users:
        c = Chat.objects.filter(from_user=u,to_user=user,seen=False).count()
        with_users_dict[u]=c

    return render(request,'cabshare/mychats.html',{'with_users_dict':with_users_dict})
# -------------------------------------------------------------------------------------------------------------------------

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    notifications = notifications.order_by('-pk')
    unseen = Notification.objects.filter(to_user=user,seen=False).count()
    notify=notifications.filter(seen=False)
    for n in notify:
        n.seen = True
        n.save()
    return render(request,'cabshare/notifications.html',{'notifications':notifications,'unseen':unseen})

@login_required
def notify_delete_all(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    for n in notifications:
        n.delete()
    return redirect('cabshare:notifications')

# -------------------------------------------------------------------------------------------------------------------------

@login_required
def drop_booking(request):
    pk = request.GET.get('inputValue')
    b = Booking.objects.get(pk=pk)
    b.drop=True
    b.save()
    data = {
        'pk': pk
            }

    return JsonResponse(data)

@login_required
def make_active(request):
    pk = request.GET.get('inputValue')
    b = Booking.objects.get(pk=pk)
    b.drop=False
    b.save()
    data = {
        'pk': pk
            }

    return JsonResponse(data)

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request,'Thanks for the feedback. We try our best to give you the best.')
            return redirect('cabshare:index')
        else:
            render(request,'cabshare/feedbackform.html',{'form':form})
    else:
        form = FeedbackForm(None)
        return render(request,'cabshare/feedbackform.html',{'form':form})
