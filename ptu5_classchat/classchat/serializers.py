from rest_framework import serializers
from . import models


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')
        
    class Meta:
            model = models.PostComment
            fields = ('id', 'post', 'post_comment', 'user', 'user_id', 'created_at')



class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = PostCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return models.PostComment.objects.filter(post=obj).count()
        
    class Meta:
            model = models.Post
            fields = ('id', 'subject', 'title', 'body', 'user', 'user_id', 'created_at', 'comments', 'comments_count')
