from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User_profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'account/home.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('account:profile-add')

        return render(request, 'account/registration_form.html',{'form':form})
    else:
        form = UserForm(None)
        return render(request, 'account/registration_form.html',{'form':form})

def login_user(request):
        username = request.GET.get('username')
        password = request.GET.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('account:login-redirect')
        else:
            messages.error(request, 'The credentials you entered were wrong.Please try again.')
            return render(request,'account/home.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('account:home')

def loginredirect(request):
    try:
        user_profile = User_profile.objects.get(user = request.user)
    except User_profile.DoesNotExist:
        return redirect('account:profile-add')
    else:
        return redirect('cabshare:index')

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = User_profile
    fields= ['name','photo','date_of_birth','hostel','department','gender','bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileCreate, self).form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User_profile
    fields= ['name','photo','date_of_birth','hostel','department','gender','bio']

@login_required
def details(request):
    user_profile = User_profile.objects.get(user = request.user)
    context = {
    'user_profile':user_profile
    }
    return render(request,'account/detail.html',context)

@login_required
def profile(request,pk):
    user = User.objects.get(pk=pk)
    user_profile = User_profile.objects.get(user = user)
    context = {
    'user_profile':user_profile
    }
    return render(request,'account/detail.html',context)
