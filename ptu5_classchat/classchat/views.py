from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models, serializers



class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentList(generics.ListCreateAPIView):
    # queryset = models.Comment.objects.all()
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.PostComment.objects.filter(post=post)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Sorry! But you cannot delete this POST it is not yours'))

    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Sorry! But you cannot change this POST it is not yours'))


class PostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =models.PostComment.objects.all()
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        post = models.PostComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Sorry! But you cannot delete this COMMENT it is not yours'))

    def put(self, request, *args, **kwargs):
        post = models.PostComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Sorry! But you cannot change this COMMENT it is not yours'))
    

class PostLikeCreate(generics.CreateAPIView):
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.PostLike.objects.filter(user=user, post=post)

    def perform_create(self, serializer):
        user = self.request.user
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, post=post)

