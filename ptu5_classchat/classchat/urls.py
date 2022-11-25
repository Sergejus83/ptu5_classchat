from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('post/<int:pk>/comments/', views.PostCommentList.as_view()),
    path('comment/<int:pk>/', views.PostCommentDetail.as_view()),

]
