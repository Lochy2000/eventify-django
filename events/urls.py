# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Event URLs
    path('events/', views.EventList.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    
    # Attendance URLs
    path('attendees/', views.EventAttendeeList.as_view(), name='event-attendee-list'),
    path('attendees/<int:pk>/', views.EventAttendeeDetail.as_view(), name='event-attendee-detail'),
    path('events/<int:event_id>/attendees/', views.EventAttendeesByEvent.as_view(), name='event-attendees-by-event'),
]