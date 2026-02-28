from .views import NotificationList
from django.urls import path

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notifications'),
]