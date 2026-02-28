from django.shortcuts import render

# Create your views here.
from rest_framework import status,generics,permissions
from rest_framework.response import Response
from .serializers import SignupSerializer,ProfileSerializer,FollowSerializer
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


# Create your views here.
class SignupViewSet(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     token = Token.objects.create(user=user)
    #     return Response({'token': token.key},status=status.HTTP_201_CREATED)

class ProfileViewSet(RetrieveAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = User.objects.filter(username=username)
        return queryset


class FollowView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        current_user = self.request.user
        target_user_id = serializer.validated_data['target_user_id']
        target_user = User.objects.get(id=target_user_id)

        if target_user in current_user.following.all():
            current_user.following.remove(target_user)
            action = 'unfollowed'
        else:
            current_user.following.add(target_user)
            action = 'followed'

        current_user.save()
        serializer.instance = current_user
        return action

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = self.perform_update(serializer)
        return Response({'status': action})