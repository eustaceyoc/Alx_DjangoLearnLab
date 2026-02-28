from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='noti_recipient')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='noti_actor')
    verb = models.CharField(max_length=120)
    target = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)