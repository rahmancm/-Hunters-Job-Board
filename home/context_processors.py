from .models import Notification
from django.contrib.auth import authenticate


def notification(request):
    if request.user.is_authenticated:
        return {'notification':request.user.notifications.filter(is_read=False)}
    else:
        return {'notification':[]}   