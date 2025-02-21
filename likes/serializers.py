# likes/serializers.py
from django.db import IntegrityError
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    event_title = serializers.ReadOnlyField(source='event.title')  

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'event', 'event_title', 
            'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already liked this event'
            })