from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentListCreateView, CommentRetrieveUpdateDestroyView
from rest_framework.authtoken.views import obtain_auth_token
from .views import CommentRatingView






router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
from rest_framework.authtoken.views import obtain_auth_token


    # басқа URL-дер...




urlpatterns = [

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comments-list-create'),
    path('comments/<int:comment_id>/rate/', CommentRatingView.as_view(), name='comment-rate'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comments-detail'),
]
