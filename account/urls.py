from django.urls import path, include
from . import views
app_name = 'account'
urlpatterns = [
    path('home/',views.home,name='home'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('signup/', views.register, name='register'),
    path('profile/', views.details, name='profile-view'),
    path('profile/add', views.ProfileCreate.as_view(), name='profile-add'),
    path('redirect', views.loginredirect, name='login-redirect'),
    path('profile/<int:pk>/edit', views.ProfileUpdate.as_view(), name='profile-update'),
]
