# comments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('events/<int:event_pk>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]