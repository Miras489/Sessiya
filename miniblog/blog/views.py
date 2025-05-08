from rest_framework import viewsets, generics, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment
from .serializers import (
    PostSerializer,
    CommentSerializer,
    UserRegistrationSerializer,
    CommentRatingSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at', 'author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], author=self.request.user)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'], author=self.request.user)
        serializer.save(author=self.request.user, post=post)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Бұл комментарийді өзгертуге рұқсатыңыз жоқ!")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Бұл комментарийді жоюға рұқсатыңыз жоқ!")
        instance.delete()

class CommentRatingView(generics.CreateAPIView):
    serializer_class = CommentRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        serializer.save(user=self.request.user, comment=comment)
class CommentRatingView(generics.CreateAPIView):
    serializer_class = CommentRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        serializer.save(user=self.request.user, comment=comment)
