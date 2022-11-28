from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')
        
    class Meta:
            model = models.PostComment
            fields = ('id', 'post', 'user', 'user_id', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    post_comments = PostCommentSerializer(many=True, read_only=True)

    def get_likes_count(self, obj):
        return models.PostLike.objects.filter(post=obj).count()

    def get_comments_count(self, obj):
        return models.PostComment.objects.filter(post=obj).count()
        

    class Meta:
            model = models.Post
            fields = ('id', 'subject', 'title', 'image', 'body', 'user', 'user_id', 'created_at', 'comments_count', 'likes_count', 'post_comments', )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

