# events/views.py
from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Event, EventAttendee
from .serializers import EventSerializer, EventAttendeeSerializer
from eventify.permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    """
    List all events, or create a new event.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True),
        # Add count of attendees for each event
        attendees_count=Count('attendees', distinct=True),
        # Add count of favorites
        favorites_count=Count('favorited_by', distinct=True)
    )
    search_fields = ['title', 'owner__username', 'category']
    ordering_fields = ['date', 'likes_count', 'comments_count', 'attendees_count']
    filterset_fields = ['category', 'owner__profile']

    def perform_create(self, serializer):
        """Set the owner to the current user when creating an event"""
        # Debug logging for file uploads
        print("\n==== EVENT CREATION DEBUG ====")
        print(f"Request method: {self.request.method}")
        print(f"Request content type: {self.request.content_type}")
        print(f"Request FILES: {self.request.FILES}")
        if 'cover' in self.request.FILES:
            print(f"Cover file found: {self.request.FILES['cover'].name}, size: {self.request.FILES['cover'].size} bytes")
        else:
            print("No cover file in request")
        print("==============================\n")
            
        # Save the event
        event = serializer.save(owner=self.request.user)
        
        # Log the result
        print(f"Event created: {event.id}, cover: {event.cover}")
        return event


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True),
        # Add count of attendees for event detail
        attendees_count=Count('attendees', distinct=True),
        # Add count of favorites
        favorites_count=Count('favorited_by', distinct=True)
    )
    
    def perform_update(self, serializer):
        """Override to add debugging for image uploads during event updates"""
        # Debug logging for file uploads
        print("\n==== EVENT UPDATE DEBUG ====")
        print(f"Request method: {self.request.method}")
        print(f"Request content type: {self.request.content_type}")
        print(f"Request FILES: {self.request.FILES}")
        if 'cover' in self.request.FILES:
            print(f"Cover file found: {self.request.FILES['cover'].name}, size: {self.request.FILES['cover'].size} bytes")
        else:
            print("No cover file in update request")
        print("============================\n")
            
        # Save the event
        event = serializer.save()
        
        # Log the result
        print(f"Event updated: {event.id}, cover: {event.cover}")
        return event


# Views for event attendance/registration
class EventAttendeeList(generics.ListCreateAPIView):
    """
    List all events a user is attending, or register for a new event.
    GET: Returns list of events the current user is registered for
    POST: Register the current user for an event
    """
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only attendance records for the current user"""
        user = self.request.user
        return EventAttendee.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        """Set the owner to the current user when registering for an event"""
        serializer.save(owner=self.request.user)


class EventAttendeeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or cancel a specific event registration.
    GET: View details of a specific registration
    DELETE: Cancel registration for an event
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventAttendeeSerializer
    queryset = EventAttendee.objects.all()


class EventAttendeesByEvent(generics.ListAPIView):
    """
    List all attendees for a specific event.
    Only available to the event owner or attendees.
    """
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get attendees for a specific event if user has permission"""
        event_id = self.kwargs['event_id']
        user = self.request.user
        
        # Check if user is event owner or an attendee
        try:
            event = Event.objects.get(id=event_id)
            if event.owner == user or EventAttendee.objects.filter(event=event, owner=user).exists():
                return EventAttendee.objects.filter(event=event_id)
            return EventAttendee.objects.none()
        except Event.DoesNotExist:
            return EventAttendee.objects.none()
