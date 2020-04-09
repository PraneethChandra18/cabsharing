from django.urls import path, include
from . import views


app_name = 'cabshare'
urlpatterns = [
    path('',views.index,name='index'),
    path('mybookings/',views.details,name='my_bookings'),
    path('cb/',views.current_bookings,name='current_bookings'),
    path('booking/add', views.BookingCreate, name='booking-add'),
    path('booking/edit/<int:pk>', views.BookingUpdate.as_view(), name='booking-update'),
    path('booking/delete/<int:pk>', views.BookingDelete.as_view(), name='booking-delete'),
    path('booking/deleteall/', views.DeletePrevious, name='booking-delete-previous'),

    # path('active/',views.isactive,name='isactive'),
    path('search/',views.search,name='search'),
    path('results/<int:pk>/',views.results,name='results'),
    path('joinrequest/<int:pk>/',views.joinrequest,name='joinrequest'),
    path('cancelrequest/<int:pk>/',views.cancelrequest,name='cancelrequest'),
    path('viewrequest/<int:pk>/',views.viewrequests,name='booking-viewrequests'),
    path('acceptrequest/<int:pk>/',views.acceptrequest,name='acceptrequest'),
    path('ignorerequest/<int:pk>/',views.ignorerequest,name='ignorerequest'),
    path('myrequests/',views.myrequests,name='myrequests'),
    path('chat/<int:pk>',views.chat,name='chat'),
    path('messagesave/<int:pk>',views.messagesave,name='messagesave'),








]
