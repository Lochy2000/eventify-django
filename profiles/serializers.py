# profiles/ serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from followers.models import Follower

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        # If no avatar, return the default avatar URL
        return 'https://res.cloudinary.com/dpw2txejq/image/upload/default_profile_ju9xum'

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None
    
    def get_followers_count(self, obj):
        return Follower.objects.filter(followed=obj.owner).count()
    
    def get_following_count(self, obj):
        return Follower.objects.filter(owner=obj.owner).count()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'bio', 'location', 'avatar', 'is_owner', 'following_id',
            'followers_count', 'following_count',
        ]