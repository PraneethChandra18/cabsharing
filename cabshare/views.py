from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout


def index(request):
    if not request.user.is_authenticated:
        return redirect('account:login') 
    else:
        user = request.user
        context = {
        'user':user
        }
        return render(request,'cabshare/index.html',context)
