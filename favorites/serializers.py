# favorites/serializers.py
from rest_framework import serializers
from django.db import IntegrityError
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Favorite
        fields = [
            'id', 'owner', 'event', 'event_title',
            'created_at'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already favorited this event'
            })
