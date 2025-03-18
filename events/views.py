# events/views.py
from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, EventAttendee
from .serializers import EventSerializer, EventAttendeeSerializer
from eventify.permissions import IsOwnerOrReadOnly


class EventList(generics.ListCreateAPIView):
    """
    List all events, or create a new event.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ['title', 'owner__username', 'category']
    ordering_fields = ['date', 'likes_count', 'comments_count', 'attendees_count']
    filterset_fields = ['category', 'owner__profile']
    
    def get_queryset(self):
        """
        Custom queryset method to handle special filters like favorites
        """
        # Base queryset with annotations
        queryset = Event.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            attendees_count=Count('attendees', distinct=True),
            favorites_count=Count('favorited_by', distinct=True)
        )
        
        # Handle favorite filter - show only events favorited by current user
        if self.request.query_params.get('favorite') == 'true':
            if self.request.user.is_authenticated:
                # Get IDs of events favorited by the current user
                from favorites.models import Favorite
                favorite_event_ids = Favorite.objects.filter(
                    owner=self.request.user
                ).values_list('event_id', flat=True)
                
                # Filter events to only those IDs
                queryset = queryset.filter(id__in=favorite_event_ids)
                
                print(f"Filtered to {queryset.count()} favorites for user {self.request.user.username}")
            else:
                # No favorites for unauthenticated users
                queryset = queryset.none()
        
        # Handle 'attending=true' filter similar to favorites
        if self.request.query_params.get('attending') == 'true':
            if self.request.user.is_authenticated:
                # Get IDs of events the user is attending
                attendance_event_ids = EventAttendee.objects.filter(
                    owner=self.request.user
                ).values_list('event_id', flat=True)
                
                # Filter events to only those IDs
                queryset = queryset.filter(id__in=attendance_event_ids)
                
                print(f"Filtered to {queryset.count()} events user {self.request.user.username} is attending")
            else:
                # No events for unauthenticated users
                queryset = queryset.none()
                
        return queryset

    def perform_create(self, serializer):
        """Set the owner to the current user when creating an event"""
        # Debug logging for file uploads
        print("\n==== EVENT CREATION DEBUG ====")
        print(f"Request method: {self.request.method}")
        print(f"Request content type: {self.request.content_type}")
        print(f"Request FILES: {self.request.FILES}")
        print(f"Request data keys: {self.request.data.keys()}")
        if 'cover' in self.request.FILES:
            print(f"Cover file found: {self.request.FILES['cover'].name}, size: {self.request.FILES['cover'].size} bytes")
            file_content = self.request.FILES['cover'].read(50)  # Read first 50 bytes
            self.request.FILES['cover'].seek(0)  # Reset file pointer
            print(f"First bytes of file: {file_content}")
        else:
            print("No cover file in request")
            if 'cover' in self.request.data:
                print(f"Cover in request.data: {type(self.request.data['cover'])}")
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
    GET: Returns list of events the user is registered for (can filter by owner__username)
    POST: Register the current user for an event
    """
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'owner__username', 'event'] 
    
    def get_queryset(self):
        """Return all attendance records with the ability to filter"""
        # Check if specific owner username is requested
        username = self.request.query_params.get('owner__username', None)
        if username:
            # If we have a username parameter, filter by that username
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(username=username)
                return EventAttendee.objects.filter(owner=user)
            except User.DoesNotExist:
                return EventAttendee.objects.none()
        # If no username specified, default to current user for backwards compatibility
        return EventAttendee.objects.filter(owner=self.request.user)
    
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
