from .models import Notification
from django.contrib.auth import authenticate


def notification(request):
    if request.user.is_authenticated:
        return {'notifications':request.user.notifications.filter(is_read=False)}
    else:
        return {'notifications':[]}   