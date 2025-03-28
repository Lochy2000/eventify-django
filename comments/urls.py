# comments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]