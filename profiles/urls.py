from django.urls import path
from profiles import views
from profiles.views import ProfileList

urlpatterns = [
    path('profiles/', views.ProfileList.as_view(), name = 'profile-list'),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view(), name = 'profile-details'),
]