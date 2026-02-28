from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer,LikeSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering_field = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering_field = '-created_at'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikeView(GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {'message': 'You already liked this post'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="Liked your post",
            target=post.title,
        )

        return Response(
            {'message': 'Post liked successfully'},
            status=status.HTTP_201_CREATED
        )


class UnLikeView(GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if Like.objects.filter(post_id=pk, user=request.user).exists():
            like = Like.objects.get(post_id=pk, user=request.user)
            like.delete()
            return Response(
                {'message': 'You unliked a post'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'You have not liked this post'},
            status=status.HTTP_201_CREATED
        )