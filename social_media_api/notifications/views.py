from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import permissions


# Create your views here.
class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
        return queryset