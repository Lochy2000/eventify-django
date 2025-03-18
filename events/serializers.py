# events/serializers.py
from rest_framework import serializers
from .models import Event, EventAttendee
from likes.models import Like
from favorites.models import Favorite
import os

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    favorite_id = serializers.SerializerMethodField()
    favorites_count = serializers.ReadOnlyField()
    # Add fields for event attendance
    attendees_count = serializers.ReadOnlyField()
    attendance_id = serializers.SerializerMethodField()  # To track current user's attendance
    # Make cover an explicit image field to ensure proper handling
    cover = serializers.ImageField(required=False)



    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, event=obj).first()
            return like.id if like else None
        return None

    def get_favorite_id(self, obj):
        """Get favorite ID for the current user only"""
        user = self.context['request'].user
        if user.is_authenticated:
            # Only return favorite ID if the current user has favorited this event
            favorite = Favorite.objects.filter(owner=user, event=obj).first()
            return favorite.id if favorite else None
        return None
        
    # Get attendance ID for the current user if they're registered
    def get_attendance_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            attendance = EventAttendee.objects.filter(owner=user, event=obj).first()
            return attendance.id if attendance else None
        return None

    def validate_cover(self, value):
        """Custom validation for cover field"""
        if value is None:
            return value
            
        print(f"Validating cover: {type(value)}, value: {value}")
            
        # Check file size (10MB limit)
        if hasattr(value, 'size') and value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large ( > 10MB )")
        
        # Check file type
        if hasattr(value, 'content_type') and not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File is not an image")
            
        return value
        
    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title',
            'description', 'date', 'location', 'category', 'cover',
            'price', 'is_owner', 'like_id', 'likes_count', 'comments_count',
            'favorite_id', 'favorites_count', 'attendees_count', 'attendance_id'
        ]


# Serializer for event attendance/registration
class EventAttendeeSerializer(serializers.ModelSerializer):
    """
    Serializer for EventAttendee model, handling event registrations.
    Includes convenience fields for easier frontend rendering.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    event_title = serializers.ReadOnlyField(source='event.title')
    event_date = serializers.ReadOnlyField(source='event.date')
    # Use a SerializerMethodField to convert Cloudinary field to URL string
    event_image = serializers.SerializerMethodField()
    
    # Convert CloudinaryResource to string URL to make it JSON serializable
    def get_event_image(self, obj):
        if obj.event.cover:
            # Convert the CloudinaryResource to its URL string representation
            return str(obj.event.cover)
        return None
    
    class Meta:
        model = EventAttendee
        fields = [
            'id', 'owner', 'event', 'registered_at', 
            'event_title', 'event_date', 'event_image'
        ]
