# favorites/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.FavoriteList.as_view(), name='favorite-list'),
    path('favorites/<int:pk>/', views.FavoriteDetail.as_view(), name='favorite-detail'),
]