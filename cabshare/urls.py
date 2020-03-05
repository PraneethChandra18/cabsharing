from django.urls import path, include
from . import views
app_name = 'cabshare'
urlpatterns = [
    path('',views.index,name='index'),

]
