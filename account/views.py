from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'account/registration_form.html'
#     # if method = get then the page shows blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form':form})
#     # if method = post, then the page processess form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             user = form.save(commit=False)
#
#             #cleaned (normalized) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#
#             # returns User objects if credentials are correct
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('cabshare:index')
#
#         return render(request, self.template_name, {'form':form})

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
                    return redirect('cabshare:index')

        return render(request, 'account/registration_form.html',{'form':form})
    else:
        form = UserForm(None)
        return render(request, 'account/registration_form.html',{'form':form})



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        data = request.POST.copy()

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('cabshare:index')
        else:
            return render(request,'account/login_form.html',{'form':form})
    else:
        form = LoginForm(None)
        return render(request,'account/login_form.html',{'form':form})



def logout_user(request):
    logout(request)
    return redirect('account:login')
