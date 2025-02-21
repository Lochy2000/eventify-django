# events/serializers.py
from rest_framework import serializers
from .models import Event
from likes.models import Like

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, event=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title',
            'description', 'date', 'location', 'category', 'cover',
            'price', 'is_owner', 'like_id', 'likes_count', 'comments_count'
        ]
