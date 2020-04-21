from .models import User,Notification

def notifications_all(request):
    if request.user.is_authenticated:
        user = request.user
        notifications_all = Notification.objects.filter(to_user=user,seen=False)
        return {"notifications_all": notifications_all}
    else:
        x = 0
        return {"notifications_all": 0}

def logged_in_user(request):
    if request.user.is_authenticated:
        user = request.user
        return {'logged_in_user':user}
    else:
        x = 0
        return {"notifications_all": 0}
