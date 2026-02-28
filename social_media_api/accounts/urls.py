from django.urls import path
from .views import SignupViewSet,ProfileViewSet,FollowView
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("register/", SignupViewSet.as_view(), name="register"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path('follow/<int:user_id>', FollowView.as_view(), name='follow-toggle'),
    path('unfollow/<int:user_id>/', FollowView.as_view(), name='unfollow-toggle'),
    path("profile/<str:username>/", ProfileViewSet.as_view(), name="profile"),
]