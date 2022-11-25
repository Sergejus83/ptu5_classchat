from django.shortcuts import render
from rest_framework import generics, permissions
from . import models, serializers


class PostList(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
