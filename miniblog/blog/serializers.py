from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment, CommentRating

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class CommentRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CommentRating
        fields = ['id', 'user', 'comment', 'rating']
        read_only_fields = ['id', 'user', 'comment']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at', 'author', 'likes', 'dislikes']
        read_only_fields = ['id', 'created_at', 'author', 'post', 'likes', 'dislikes']

    def get_likes(self, obj):
        return obj.ratings.filter(rating='like').count()

    def get_dislikes(self, obj):
        return obj.ratings.filter(rating='dislike').count()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'comments']
        read_only_fields = ['id', 'created_at', 'author', 'comments']
class CommentRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CommentRating
        fields = ['id', 'user', 'comment', 'rating']
        read_only_fields = ['id', 'user', 'comment']
