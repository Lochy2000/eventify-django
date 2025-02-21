# likes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('likes/', views.LikeList.as_view(), name='like-list'),
    path('likes/<int:pk>/', views.LikeDetail.as_view(), name='like-detail'),
]