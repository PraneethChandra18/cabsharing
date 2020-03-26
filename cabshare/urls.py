from django.urls import path, include
from . import views


app_name = 'cabshare'
urlpatterns = [
    path('',views.index,name='index'),
    path('mybookings/',views.details,name='my_bookings'),
    path('cb/',views.current_bookings,name='current_bookings'),
    path('booking/add', views.BookingCreate.as_view(), name='booking-add'),
    path('booking/edit/<int:pk>', views.BookingCreate.as_view(), name='booking-update'),
    path('booking/delete/<int:pk>', views.BookingDelete.as_view(), name='booking-delete'),
    path('active/',views.isactive,name='isactive'),

]
