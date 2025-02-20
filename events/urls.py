from django.urls import path
from events import views

urlpatterns = [
    path('events/', views.EventList.as_view(), name='event-list'),  # Add name
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),  # Add name
    path('events/<int:pk>/like/', views.LikeCreate.as_view(), name='like-create'),
    path('likes/<int:pk>/', views.LikeDestroy.as_view(), name='like-destroy'),
    path('events/<int:event_pk>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]
 